
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from unidecode import unidecode
from . import models

from .models import UserProfile, Ritsep, Comment, Rating
from .forms import UserForm,ProfileUpdateForm ,ProfileUpdateForm, PostCreateForm,PostUpdateForm,CommentForm,RatingForm,RegisterForm,LoginForm


User = get_user_model()


def normalize(text):
    if text:
        return unidecode(text).lower()
    return ""


def home(request):
    return render(request, "home.html")


def user_list(request):
    query = request.GET.get("q")
    users = User.objects.all()

    if query:
        q = normalize(query)
        users = [user for user in users if q in normalize(user.first_name) or q in normalize(user.last_name)]

    return render(request,"index.html", {"users": users})

# @login_required
def user_detail(request,slug):  
    user=get_object_or_404(User,slug=slug)
    return render(request,"user_detail.html", {"user": user})


def user_create(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("user_list")

    else:
        form = UserForm()

    return render(request,"user_create.html",{"form": form})

@login_required
def user_update(request, slug):

    user = get_object_or_404(User,slug=slug)

    if request.method == "POST":

        form = UserForm(request.POST,request.FILES,instance=user)

        if form.is_valid():
            form.save()
            return redirect("user_detail",slug=user.slug)

    else:
        form = UserForm(instance=user)

    return render(request,"user_update.html",{"form": form})


def user_delete(request, slug):

    user = get_object_or_404(
        User,
        slug=slug
    )

    if request.method == "POST":
        user.delete()
        return redirect("user_list")

    return render(
        request,
        "user_delete.html",
        {
            "user": user
        }
    )


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.method == "POST":

        form = LoginForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            return redirect("post_list")

    else:
        form = LoginForm()

    return render(
        request,
        "login.html",
        {
            "form": form
        }
    )


def logout_view(request):
    logout(request)
    return redirect("home")


# @login_required
def profile(request, slug):

    user = get_object_or_404(
        User,
        slug=slug
    )

    profile = get_object_or_404(
        UserProfile,
        user=user
    )

    posts = Ritsep.objects.filter(
        author=user
    )

    return render(
        request,
        "profile.html",
        {
            "user": user,
            "profile": profile,
            "posts": posts
        }
    )


# @login_required
# def userprofile_update(request, slug):

#     profile = get_object_or_404(
#         UserProfile,
#         user__slug=slug
#     )

#     if request.method == "POST":

#         form = UserProfileUpdateForm(
#             request.POST,
#             instance=profile
#         )

#         if form.is_valid():
#             form.save()

#             return redirect(
#                 "profile",
#                 slug=slug
#             )

#     else:

#         form = UserProfileUpdateForm(
#             instance=profile
#         )

#     return render(
#         request,
#         "userprofile_update.html",
#         {
#             "form": form
#         }
#     )


@login_required
def profile_update(request, slug):

    profile = get_object_or_404(
        UserProfile,
        user__slug=slug
    )

    if request.method == "POST":

        form = ProfileUpdateForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            form.save()

            return redirect(
                "profile",
                slug=slug
            )

    else:

        form = ProfileUpdateForm(
            instance=profile
        )

    return render(
        request,
        "profile_update.html",
        {
            "form": form
        }
    )


@login_required
def profile_delete(request, slug):

    user = get_object_or_404(
        User,
        slug=slug
    )

    if request.method == "POST":
        user.delete()
        return redirect("user_list")

    return render(
        request,
        "profile_delete.html",
        {
            "user": user
        }
    )


def post_list(request):

    posts = Ritsep.objects.all().order_by("-created_at")

    return render(
        request,
        "post_list.html",
        {
            "posts": posts
        }
    )


def post_detail(request, slug):

    post = get_object_or_404(
        Ritsep,
        slug=slug
    )

    return render(
        request,
        "post_detail.html",
        {
            "post": post
        }
    )


@login_required          
def post_create(request):

    if request.method == "POST":

        form = PostCreateForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            post = form.save(
                commit=False
            )

            post.author = request.user
            post.save()

            return redirect(
                "post_list"
            )

    else:
        form = PostCreateForm()

    return render(
        request,
        "post_create.html",
        {
            "form": form
        }
    )


@login_required
def post_update(request, slug):

    post = get_object_or_404(
        Ritsep,
        slug=slug,
        author=request.user
       
    )

    if request.method == "POST":

        form = PostUpdateForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():

            form.save()

            return redirect(
                "post_detail",
                slug=post.slug
            )

    else:

        form = PostUpdateForm(
            instance=post
        )

    return render(request,"post_update.html",{"form": form,"post": post})



@login_required
def post_delete(request, slug):

    post = get_object_or_404(Ritsep,slug=slug,author=request)

    if request.method == "POST":

        post.delete()

        return redirect("post_list")

    return render(request,"post_delete.html",{"post": post})
    
def ritsep_detail(request, slug):
    ritsep = Ritsep.objects.get(slug=slug)

    if request.method == "POST":

        if "comment_submit" in request.POST:
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.ritsep = ritsep
                comment.save()

        if "rating_submit" in request.POST:
            stars = request.POST.get("stars")

            Rating.objects.update_or_create(
                user=request.user,
                ritsep=ritsep,
                defaults={
                    "stars": stars
                }
            )

    comment_form = CommentForm()
    rating_form = RatingForm()

    context = {
        "ritsep": ritsep,
        "comment_form": comment_form,
        "rating_form": rating_form,
    }

    return render(request,"post_detail.html",context)

