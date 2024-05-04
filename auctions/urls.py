from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_item", views.create_item, name="create_item"),
    path("watchlist/<str:user_id>", views.watchlist, name="watchlist"),
    path("item/<str:item_id>", views.listing, name="listing"),
    path("closed_item/<str:item_id>", views.closed_item, name="closed_item"),
    path("add_bid", views.add_bid, name="add_bid"),
    path("add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("close_auction", views.close_auction, name="close_auction"),
]
