import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import NewPostForm
from .models import User, Post, Like, Follow


def login_view(request):
    '''Log user in'''

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    '''Log user out'''

    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    '''Register new user'''

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def index(request):
    '''Show all posts'''

    # Get all posts
    all_posts = Post.objects.all().order_by("-created")

    # Show 10 posts per page
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    list_of_page_numbers = list(range(1, page_obj.paginator.num_pages + 1))

    return render(request, "network/index.html", {"page_obj": page_obj, "page_numbers": list_of_page_numbers})


@login_required(redirect_field_name=None)
def following_content(request):
    '''Show all posts made by users that the current user follows'''

    # Get all posts form users that the current user follows
    followed_users = Follow.objects.filter(follower=request.user)
    followed_users = [followed_users[i].user for i in range(len(followed_users))]
    posts_from_followed_users = Post.objects.filter(user__in=followed_users).order_by("-created")

    # Show 10 posts per page
    paginator = Paginator(posts_from_followed_users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    list_of_page_numbers = list(range(1, page_obj.paginator.num_pages + 1))

    return render(request, "network/following.html", {"page_obj": page_obj, "page_numbers": list_of_page_numbers})


def profile_page(request, user_id):
    '''Show profile of the user'''

    # Get all profile users posts
    profile_user = User.objects.get(pk=user_id)
    users_posts = Post.objects.filter(user= profile_user).order_by("-created")

    # Show 10 posts per page
    paginator = Paginator(users_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    list_of_page_numbers = list(range(1, page_obj.paginator.num_pages + 1))

    # Check if profile is not users
    if profile_user == request.user:
        status = None
    else:
        # Check if user follows profile
        try:
            Follow.objects.get(user= profile_user, follower=request.user)

        except (ObjectDoesNotExist, TypeError): # Type error occurs in case when user is not authenticated
            status = "Follow"

        else:
            status = "Unfollow"

    params = {"username": profile_user.username,
              "user_id": user_id,
              "page_obj": page_obj,
              "page_numbers": list_of_page_numbers,
              "status": status,
              "number_of_followers": len(Follow.objects.filter(user=profile_user)),
              "number_of_following": len(Follow.objects.filter(follower=profile_user))}

    return render(request, "network/profile.html", params)


@login_required(redirect_field_name=None)
def new_post(request):
    '''Write new post'''

    form = NewPostForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            # Create new post
            text = form.cleaned_data["text"]
            new_post = Post(user=request.user, text=text)
            new_post.save()

            return redirect(reverse("index"))
        
        else:
            # Show error message if form is not valid
            print(form.errors)

            params = {"form": form, 
                      "error_message": "Try again!"}

            return render(request, "network/new_post.html", params)

    return render(request, "network/new_post.html", {"form": form})


@login_required(redirect_field_name=None)
def follow(request, user_id):
    '''Follow or unfollow user'''

    # Get profile user
    profile_user = User.objects.get(pk=user_id)

    # Error case
    if profile_user == request.user:
        # Do nothing, redirect back to profile page
        return_link = reverse("profile", args=(user_id,))
        return redirect(return_link)

    # Check if followed
    try:
        follower = Follow.objects.get(user=profile_user, follower=request.user)

    # Follow if was not followed
    except ObjectDoesNotExist:
        new_follower = Follow(user=profile_user, follower=request.user)
        new_follower.save()
        return JsonResponse({"number_of_followers": len(Follow.objects.filter(user=profile_user)), 
                             "status": "followed"})
    
    # Unfollow if was followed
    else:
        follower.delete()
        return JsonResponse({"number_of_followers": len(Follow.objects.filter(user=profile_user)), 
                             "status": "not followed"})


@login_required(redirect_field_name=None)
def like_post(request, post_id):
    '''Like or unlike post'''

    # Get post
    post = Post.objects.get(pk=post_id)

    # Check if liked
    try:
        like = Like.objects.get(user=request.user, post=post)

    # Like if not liked
    except ObjectDoesNotExist:
        post.like()
        post.save(update_fields=["number_of_likes"])
        new_like = Like(user=request.user, post=post)
        new_like.save()

    # Unlike if liked
    else:
        post.unlike()
        post.save(update_fields=["number_of_likes"])
        like.delete()

    return JsonResponse({"number_of_likes": post.number_of_likes})


@csrf_exempt
@login_required(redirect_field_name=None)
def edit_post(request, post_id):
    '''Edit existing post'''

    # Get post
    try:
        post = Post.objects.get(pk=post_id)
    
    except ObjectDoesNotExist:
        return JsonResponse({"status": "error"})

    # Get new text for post (js!)
    data = json.loads(request.body)
    new_text = data.get("new_text")

    # Error case
    if post.user != request.user or not new_text:
        return JsonResponse({"status": "error"})

    # Update text
    post.text = new_text
    post.save(update_fields=["text"])
    return JsonResponse({"status": "ok"})


@login_required(redirect_field_name=None)
def delete_post(request, post_id):
    '''Delete existing post'''
    
    # Get post
    try:
        post = Post.objects.get(pk=post_id)

    except ObjectDoesNotExist:
        return JsonResponse({"status": "error"})
    
    # Check if user is posts author
    if post.user != request.user:
        return JsonResponse({"status": "error"})
    
    # Delete post
    post.delete()
    return JsonResponse({"status": "ok"})
