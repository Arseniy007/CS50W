from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("item/<int:listing_id>", views.listing_page, name="listing_page"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("comment/<int:listing_id>", views.leave_comment, name="comment"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("my_listings", views.users_listings, name="users_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_<int:listing_id>_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.listings_in_category, name="listings_in_category")
]
