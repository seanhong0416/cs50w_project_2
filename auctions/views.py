from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionList, Bids, Comments, WatchList


def index(request):
    return render(request, "auctions/index.html", {
        "items":AuctionList.objects.all(),
    })


def login_view(request, original_page=None):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if original_page is not None:
                return HttpResponseRedirect(original_page)
            else:
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request, original_page=None):
    logout(request)
    if original_page is not None:
        return HttpResponseRedirect(original_page)
    else:
        return HttpResponseRedirect(reverse("index"))


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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def create_item(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        title = request.POST["title"]
        image = request.FILES["image"]
        description = request.POST["description"]
        type = request.POST["type"]
        starting_bid = request.POST["starting_bid"]
        owner = request.user

        new_item = AuctionList(title=title, image=image, description=description, type = type, starting_bid=starting_bid, owner=owner, is_closed=False)
        new_item.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_item.html")
    
def listing(request, item_id):
    item = AuctionList.objects.get(pk=item_id)
    user = request.user
    bids = item.bids.order_by('-price').values()
    
    if not bids:
        price = item.starting_bid
    else:
        price = bids.first().price

    #if user is None, then not logged in
    user = None
    if request.user.is_authenticated:
        user=request.user
    
    return render(request, "auctions/item.html", {
        "item":item,
        "bids":bids,
        "user":user,
        "price":price,
        "watched":item.watched,
    })

def watchlist(request, user_id):
    user = request.user
    user_watchlist = WatchList.objects.filter(watching=user)
    items = []
    for item in user_watchlist:
        items.append(item.item)

    return render(request, "auctions/index.html", {
        "items":items,
    })
    

def add_to_watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("listing", args=[item_id]))
    user = request.user
    item_id = request.POST["item_id"]
    item = AuctionList.objects.get(pk=item_id)
    new_watchllist = WatchList(watching=user, item=item)
    new_watchllist.save()

    return HttpResponseRedirect(reverse("listing", args=[item_id]))

def add_bid(request):
    pass