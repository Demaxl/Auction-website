from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _




class User(AbstractUser):
    pass

class Category(models.Model):
    code = models.CharField(max_length=40)
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.description
                                                                                                

class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    current_bid = models.DecimalField(max_digits=20, decimal_places=2, help_text="Current or starting bid")
    image = models.URLField(blank=True)

    date_created = models.DateTimeField(auto_now_add=True)

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items_for_sale")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist") 

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} by {self.seller}'




class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    bid_time = models.DateTimeField(auto_now_add=True)
    bid_amount = models.DecimalField(max_digits=20, decimal_places=2)
    


    def __str__(self):
        return f"${self.bid_amount} bid by {self.bidder} on {self.listing}"

    def __lt__(self, other_bid) -> bool:
        return self.bid_amount < other_bid.bid_amount

    def clean(self):
        current = self.listing.current_bid
        print(current, self.bid_amount)

        try:
            if self.bid_amount <= current:
                raise ValidationError(
                _('Please enter a value higher than $%(current)s'),
                params={"current": current},
                code="invalid"
                )
        except TypeError:
            pass

        if self.bidder == self.listing.seller:
            raise ValidationError(
                _(f"{self.bidder} can't bid on the listing because they are the seller"),
                code="invalid")
    
    def save(self, *args, **kwargs):
        self.listing.current_bid = self.bid_amount
        self.listing.save()
        super().save(*args, **kwargs)
    



class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    commenter = models.ForeignKey(User, on_delete=models.CASCADE)

    comment_date = models.DateTimeField(auto_now_add=True)

    text = models.TextField()


    def __str__(self):
        return f"{self.commenter}: {self.text}"
    