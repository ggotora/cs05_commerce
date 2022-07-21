from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max


from .models import User, Listing, Bid
from .forms import BidForm, ListingForm


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
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


def new_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return redirect('/')
    form = ListingForm()
    return render(request, "auctions/new_listing.html", {
        "form": form
    })

def listing(request, listing_id):
    # watchlist 
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing.watchlist.filter(id=request.user.id).exists():
        added = True
    else:
        added = False
    
    #bid
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.listing = listing 
            instance.bid_by = request.user 
            if listing.current_price():
                if listing.current_price() >= instance.price:
                    messages.error(request, f"You only bid $ {instance.price}. Your bid must be greater the current price of ${listing.current_price():.2f}")
                    return redirect('listing', listing_id)
                else:
                    instance.save()
                    messages.info(request, f"Congradulations!! You have the highest current bid ${listing.current_price():.2f}")
                    return redirect('listing', listing_id)
            elif instance.price <= listing.starting_price:
                messages.error(request, f"You only bid ${instance.price}. Your starting bid must be greater than ${listing.starting_price:.2f}")
                return redirect('listing', listing_id)

            else:
                instance.save()
                return redirect('listing', listing_id)
            
    else:
        form = BidForm()
    context = {
        "listing": listing, 
        "added": added, 
        "form": form, 



    }
    return render(request, "auctions/listing.html", context )

@login_required(login_url="login")
def add_remove_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    added = False
    if listing.watchlist.filter(id=request.user.id).exists():
        listing.watchlist.remove(request.user)
        added = False
    else:
        listing.watchlist.add(request.user)
        added = True
    return redirect('listing', listing_id)



    
    
    