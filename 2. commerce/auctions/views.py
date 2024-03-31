from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import NewListingForm, NewBidForm, NewCategoryForm, NewCommentForm
from .models import User, Listing, Bid, Category, Comment


# Default cover for listing
default_cover = "https://st2.depositphotos.com/1561359/12101/v/950/depositphotos_121012076-stock-illustration-blank-photo-icon.jpg"


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


def index(request):
    '''Show Active Listings Page'''

    params = {"listings": Listing.objects.filter(active=True)}
    return render(request, "auctions/index.html", params)


@login_required(redirect_field_name=None)
def create_listing(request):
    '''Create new listing'''
  
    form = NewListingForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            # Handle listing cover (set default one, if none provided)
            listing_cover = form.cleaned_data["cover"]
            if not listing_cover:
                listing_cover = default_cover

            # Create and save listing model based on submitted form
            title, description = form.cleaned_data["title"], form.cleaned_data["description"]
            start_bid, category = form.cleaned_data["start_bid"], form.cleaned_data["category"]
            
            new_listing = Listing(user=request.user, cover=listing_cover, 
                                  title=title, description=description, 
                                  start_bid=start_bid, category=category)
            
            new_listing.save()

            return redirect(reverse("index"))
        
        else:
            # Show error message if form is not valid
            print(form.errors)

            params = {"form": form, 
                      "error_message": "Try again!"}
            
            return render(request, "auctions/create_listing.html", params)

    params = {"form": form}
    return render(request, "auctions/create_listing.html", params)


def listing_page(request, listing_id):
    '''Show page with an existing listing'''

    # Check if listing exists
    try:
        listing = get_object_or_404(Listing, pk=listing_id)

    except Http404:
        # Show error message
        params = {"error_message": "Listing not found"}
        return render(request, "auctions/error_page.html", params)
    
    # Get current bid
    all_bids = Bid.objects.filter(listing=listing_id).order_by("-created")
    if all_bids:
        curent_bid = all_bids[0]
    else:
        curent_bid = None

    # Get all comments
    all_comments = Comment.objects.filter(listing=listing_id).order_by("-created")

    # Get watchlist status
    if request.user in listing.watchlist.all():
        watchlist = True
    else:
        watchlist = False

    params = {"listing": listing,
            "current_bid": curent_bid,
            "all_comments": all_comments,
            "watchlist": watchlist,
            "new_bid_form": NewBidForm(),
            "new_comment_form": NewCommentForm()}
    
    return render(request, "auctions/listing_page.html", params)


@login_required(redirect_field_name=None)
def place_bid(request, listing_id):
    '''Place new bid on given listing'''

    # Get amount of new bid
    form = NewBidForm(request.POST)

    if form.is_valid():

        # Get input
        amount = form.cleaned_data["amount"]

        # Get current listing and all bids on it
        listing = Listing.objects.get(pk=listing_id)
        previous_bids = Bid.objects.filter(listing=listing_id)

        # Find highest bid
        if previous_bids:
            highest_bid = previous_bids.order_by("-created")[0].amount
        else:
            highest_bid = listing.start_bid

        if amount > highest_bid:
            # Save new bid
            new_bid = Bid(user=request.user, listing=listing, amount=amount)
            new_bid.save()

            # Redirect back to listing page
            return_link = reverse("listing_page", args=(listing_id,))
            return redirect(return_link)
    
    # Show error message
    params = {"error_message": "Invalid Bid"}
    return render(request, "auctions/error_page.html", params)


@login_required(redirect_field_name=None)
def leave_comment(request, listing_id):
    '''Leave a comment for given listing'''

    form = NewCommentForm(request.POST)

    if form.is_valid():
        
        # Get input
        text = form.cleaned_data["text"]
        headline = form.cleaned_data["headline"]

        # Get current listing
        current_listing = Listing.objects.get(pk=listing_id)

        # Create new comment
        new_comment = Comment(user=request.user, listing=current_listing, text=text, headline=headline)
        new_comment.save()

        # Redirect back to listing page
        return_link = reverse("listing_page", args=(listing_id,))
        return redirect(return_link)

    # Show error message
    params = {"error_message": "Invalid Bid"}
    return render(request, "auctions/error_page.html", params)


@login_required(redirect_field_name=None)
def close_auction(request, listing_id):
    '''Close auction for given listing and announce winner'''

    # Check if listing exists
    try:
        listing = get_object_or_404(Listing, pk=listing_id)

    except Http404:
        pass

    # Ensure user is creator of the listing and listing is active
    if listing.user == request.user and listing.active:

        # Get current bid and its author
        current_bid = Bid.objects.filter(listing=listing_id).order_by("-created")[0]
        winner = current_bid.user

        # Declare winner and close auction
        listing.winner = winner
        listing.active = False
        listing.save(update_fields=["winner", "active"])

        # Redirect back to listing page
        return_link = reverse("listing_page", args=(listing_id,))
        return redirect(return_link)

    params = {"error_message": "Something went wrong"}
    return render(request, "auctions/error_page.html", params)


@login_required(redirect_field_name=None)
def users_listings(request):
    '''Show all users listings'''

    params = {"users_listings": Listing.objects.filter(user=request.user),
              "closed_listings": Listing.objects.filter(winner=request.user)}

    return render(request, "auctions/users_listings.html", params)


@login_required(redirect_field_name=None)
def watchlist(request):
    '''Show watchlist page'''

    params = {"watchlist": Listing.objects.filter(watchlist=request.user)}

    return render(request, "auctions/watchlist.html", params)


@login_required(redirect_field_name=None)
def add_to_watchlist(request, listing_id):
    '''Add listning to watchlist or removes it from watchlist'''

    # Check if listing exists
    try:
        listing = get_object_or_404(Listing, pk=listing_id)

    except Http404:
        # Show error message
        params = {"error_message": "Listing not found"}
        return render(request, "auctions/error_page.html", params)
    
    # Check if listing is in watchlist or not
    user = request.user

    watchlist = Listing.objects.filter(watchlist=user)

    if listing in watchlist:
       listing.watchlist.remove(user)
        
    else:
        listing.watchlist.add(user)

    # Redirect back to listing page
    return_link = reverse("listing_page", args=(listing_id,))
    return redirect(return_link)
    

def categories(request):
    '''Show all categories'''

    form = NewCategoryForm(request.POST or None)

    # Add new category
    if request.method == "POST" and form.is_valid():

        new_category_name = form.cleaned_data["name"]

        new_category = Category(name=new_category_name)
        new_category.save()

        return redirect(reverse("categories"))
    
    # Get all catogries
    all_categories = Category.objects.all()

    # Count number of listings in every category
    categories_with_counter = dict()
    for category in all_categories:
        categories_with_counter[category] = len(Listing.objects.filter(category=category))

    params = {"categories": categories_with_counter, 
              "form": form}
    
    return render(request, "auctions/categories.html", params)


def listings_in_category(request, category_id):
    '''Show all listings in given category'''

    # Sort all listings by their category
    params = {"listings": Listing.objects.filter(category=category_id), 
            "category_name": Category.objects.get(pk=category_id)}
    
    return render(request, "auctions/listings_in_category.html", params)
