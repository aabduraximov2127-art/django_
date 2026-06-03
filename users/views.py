from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login as auth_login,
    logout
)
from unidecode import unidecode

from . import models 
from .forms import UserForm, RegisterForm, LoginForm, UserProfileUpdateForm, ProfileUpdateForm,PostForm
from .models import Post


 
from django.contrib.auth.decorators import login_required


User = get_user_model()
# users information
def user_list(request):
    users = User.objects.all()
    query = request.GET.get("q")
    users = User.objects.all()

    if query:
        q = normalize(query)

        users = [
            u for u in users
            if q in normalize(u.first_name)
        ]
    return render(request, "index.html", {"users": users})

def normalize(text):
    if text:
        return unidecode(text).lower()
    return ""



def home(request):
    user = request.user
    return render(request, "home.html")



def user_create(request):

    if request.method == "POST":

        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("user_list")

    else:
        form = UserForm()

    return render(request, "user_create.html", {
        "form": form
    })



def user_update(request, slug):

    user = get_object_or_404(User, slug=slug)

    if request.method == "POST":

        form = UserForm(
            request.POST,
            request.FILES,
            instance=user
        )

        if form.is_valid():
            form.save()
            return redirect("user_list")

    else:
        form = UserForm(instance=user)

    return render(request, "user_update.html", {
        "form": form
    })



def user_delete(request, id):

    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user.delete()
        return redirect("user_list")

    return render(request, "user_delete.html", {"user": user})


def user_detail(request,slug):
    user = get_object_or_404(User, slug=slug)
    return render(request, "user_detail.html", {"user": user})


# registration, login, logout
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login(request):

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()
            auth_login(request, user)
        
        
            return redirect("user_list")

    else:
        form = LoginForm()

    return render(request, "login.html", {
        "form": form
    })



def logout_view(request):
    logout(request)
    return redirect("home")
# <-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-->->->->->->->->->->->->->->->->->->->->->->->->->->->->->



# User Profile Views
def profile(request, slug):
    profile = get_object_or_404(models.ControlUsers, slug=slug)
    return render(request, "profile.html", {"profile": profile})

def userprofile_update(request, slug):
    profile = get_object_or_404(models.ControlUsers, slug=slug)

    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_detail", slug=profile.slug)
    else:
        form = UserProfileUpdateForm(instance=profile)

    return render(request, "userprofile_update.html", {"form": form})

def profile_delete(request, slug):
    profile = get_object_or_404(models.ControlUsers, slug=slug)

    if request.method == "POST":
        profile.delete()
        return redirect("user_list")

    return render(request, "profile_delete.html", {"profile": profile})

def profile_update(request, slug):
    profile = get_object_or_404(models.ControlUsers, slug=slug)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, "profile_update.html", {"form": form})


# <--------------------------------------------->
# posts
from .forms import PostUpdateForm,PostDeleteForm,PostDetailForm,PostCreateForm


def post_list(request):
    posts = Post.objects.select_related('author').all()
    return render(request, "post_list.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(models.Post, slug=slug)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect("post_detail", slug=post.slug)
    else:
        form = PostCreateForm()
    return render(request, "post_create.html", {"form": form})

@login_required
def post_update(request, slug): 
    post = get_object_or_404(models.Post, slug=slug)

    if request.method == "POST":
        form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect("post_detail", slug=post.slug)
    else:
        form = PostUpdateForm(instance=post)

    return render(request, "post_update.html", {"form": form})
@login_required
def post_delete(request, slug):
    post = get_object_or_404(models.Post, slug=slug)
    if request.method == "POST":
        form = PostDeleteForm(request.POST, instance=post)
        if form.is_valid():
            post.author = request.user
            post.delete()
            return redirect("post_list")
    return render(request, "post_delete.html", {"post": post})

