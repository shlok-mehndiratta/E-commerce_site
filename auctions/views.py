from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import Create_Listing_form
from .models import User, Category, Listings, Bids, Comments




def index(request):
    activelistings = Listings.objects.filter(isActive=True)
    allcategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activelistings,
        "categories": allcategories
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



def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            'form': Create_Listing_form()
        })

    if request.method == "POST":
        form = Create_Listing_form(request.POST)
        if form.is_valid():
            # Get the cleaned form data
            starting_bid_amount = form.cleaned_data['starting_bid']
            other_category = form.cleaned_data.get('other_category')

            # Create the Listings object, but don't save it yet
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.isActive = True

            # Create the Bids object (starting price)
            bid_obj = Bids.objects.create(bid=starting_bid_amount, user=request.user, listing=listing)

            listing.price = bid_obj  # link the created bid to the listing

            # Handle "Other" category if specified
            if other_category:
                category_obj, _ = Category.objects.get_or_create(categoryName=other_category)
                listing.category = category_obj

            # Save the listing after all modifications
            listing.save()

            # Check if listing is in user's watchlist (initially not)
            isListingInWatchlist = request.user in listing.watchlist.all()

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "isListingInWatchlist": isListingInWatchlist
            })

        else:
            # Re-render the form with errors
            return render(request, "auctions/create.html", {
                'form': form
            })

            
    
def listing(request, id):
    listingdata = Listings.objects.get(pk=id)
    isListingInWatchlist = request.user in listingdata.watchlist.all()
    # Handle update message from GET parameter
    update = request.GET.get('update')
    if update == 'success':
        message = True
        update = 'True'
    elif update == 'fail':
        message = True
        update = 'False'
    else:
        message = False
        update = None

    return render(request, "auctions/listing.html", {
        "listing": listingdata,
        "isListingInWatchlist": isListingInWatchlist,
        "message": message,
        "update": update,
    })


def displaycategory(request):
    if request.method == "POST":
        selected_cat = request.POST['category']
        category = Category.objects.get(categoryName=selected_cat)
        activelistings = Listings.objects.filter(isActive=True, category=category)
        allcategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activelistings,
            "categories": allcategories
        })


def watchlist(request):
    if request.method == "POST":
        task = request.POST["todo"]
        id = request.POST["id"]
        listingdata = Listings.objects.get(pk=id)
        currentUser = request.user
        if task == 'add':
            listingdata.watchlist.add(currentUser)
        elif task == 'remove':
            listingdata.watchlist.remove(currentUser)
        return HttpResponseRedirect(reverse("listing", args=(id, )))
    else:
        currentuser = request.user
        listings = currentuser.userwatchlist.all()
        return render(request, "auctions/watchlist.html", {
            'listings': listings
        })


def addbid(request):
    if request.method == 'POST':
        newbid = request.POST['newbid']
        id = request.POST['id']
        listingdata = Listings.objects.get(pk=id)

        if int(newbid) > listingdata.price.bid:
            updatebid = Bids(user=request.user, bid=int(newbid), listing=listingdata)
            updatebid.save()
            listingdata.price = updatebid
            listingdata.save()
            return HttpResponseRedirect(f'/listing/{id}?update=success')     
        else:
            return HttpResponseRedirect(f'/listing/{id}?update=fail')
    