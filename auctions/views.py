from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User

Choices =  [
    ('', '---------'),  # Optional empty selection
    ('home', 'Home'),
    ('toys', 'Toys'),
    ('fashion', 'Fashion'),
    ('electronics', 'Electronics'),
    ('other', 'Other (Specify Below)'),
]

class Create_Listing_form(forms.Form):
    title = forms.CharField(label='Title')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    start_bid = forms.IntegerField(label='Starting Bid')
    img_url = forms.ImageField(label="Image url", required=False)
    category = forms.ChoiceField(choices=Choices, label='Category', required=False)
    other_category = forms.CharField(required=False, label='Other (Specify)', widget=forms.TextInput(attrs={'placeholder': 'Specify other category'}))


def index(request):
    return render(request, "auctions/index.html")


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