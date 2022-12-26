from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse, reverse_lazy


from .models import User, Listing, Bid, Comment, Category

from .forms import CreateForm

from pprint import pprint 


def listings_view(request):
    listings = Listing.objects.all()

    return render(request, "auctions/listings.html", {
        "heading": "Active Listings",
        "listings": Listing.objects.exclude(is_active=False),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]


        user = authenticate(request, username=username, password=password)
        next_url = request.POST['next'].lstrip('/')
        print(next_url)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(next_url))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                "next": next_url
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("listings"))

        try:
            next_url = request.GET['next']
        except: 
            next_url = 'listings'

        return render(request, "auctions/login.html", {
            "next": next_url
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("listings"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("listings"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("listings"))

        return render(request, "auctions/register.html")


@login_required(login_url=reverse_lazy('login'))
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid(): # If the form is valid
            data = form.cleaned_data
            
            kwargs = {
                'title': data['title'],
                'description': data['description'],
                'current_bid': data['price'],
                'image': data['image'],
                'seller': request.user,
                'category': Category.objects.get(code=data['category'])
            }
            l = Listing.objects.create(**kwargs)
            l.save()

            return HttpResponseRedirect(reverse("listings"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })

    return render(request, 'auctions/create.html', {
        "form": CreateForm()
    })


def all_categories_view(request):
    categories = Category.objects.all()
        
    return render(request, 'auctions/categories.html', {
        "categories": categories
    })


def category_view(request, code):

    try:
        category = Category.objects.get(code=code)
    except Category.DoesNotExist:
        return render(request, "auctions/category_page.html", {
        "category": "404 Not Found"
    })

    return render(request, "auctions/listings.html", {
        "heading": category,
        "listings": category.listings.all()
    })

@login_required(login_url=reverse_lazy('login'))
def watchlist_view(request):
    return render(request, "auctions/listings.html", {
        "heading": "Items you are watching",
        "listings": request.user.watchlist.all(),
        "error": "You are not watching any items"
    })


def listing_page_view(request, id):
    listing = Listing.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        if "watchlist" in data:
            if data['watchlist'] == "add":
                listing.watchers.add(request.user)
            else:
                listing.watchers.remove(request.user)

        elif "close" in data:
            listing.is_active = False
            listing.save()

        elif "comment" in data:
            comment = Comment.objects.create(listing=listing, commenter=request.user, text=data['comment'])
            comment.save()

        else:
            bid = Bid.objects.create(listing=listing, bidder=request.user, bid_amount=int(data['bid']))
            bid.save()
        

    bids = listing.bids.all()

    if bids:
        highest_bidder = {'user': max(bids).bidder.username, 'price':listing.current_bid}
    else:
        highest_bidder = {'user': None, "price":listing.current_bid}

    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "bids": listing.bids.all(),
        "highest_bidder" : highest_bidder,
        "comments": listing.comments.all()
    })