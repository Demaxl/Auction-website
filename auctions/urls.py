from django.urls import path

from . import views

urlpatterns = [
    path("", views.listings_view, name="listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories", views.all_categories_view, name="categories"),
    path("categories/<str:code>/", views.category_view, name="category_page"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("listings/<int:id>", views.listing_page_view, name="listing_page")
]
