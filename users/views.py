
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model,login,logout


from django.contrib.auth.decorators import login_required
from unidecode import unidecode
from . import models
from django.db.models import F,Q

from .models import UserProfile, Post, Comment,Likes
from .forms import UserForm,ProfileUpdateForm ,ProfileUpdateForm,RegisterForm,LoginForm,PostCreateForm,PostUpdateForm,CommentForm


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

        form = RegisterForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request,"register.html",{"form": form})


def login_view(request):

    if request.method == "POST":

        form = LoginForm(request,data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request,user)

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

    posts = Post.objects.filter(
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

    posts = Post.objects.all().order_by("-created_at")

    return render(
        request,
        "post_list.html",
        {
            "posts": posts})


def post_detail(request,slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    Post.objects.filter(slug=post.slug).update(view_count=F("view_count") + 1)

    comments = post.comments.all()

    comment_form = CommentForm()

    user_liked = False

    if request.user.is_authenticated:

        user_liked = Likes.objects.filter(
            user=request.user,
            post=post
        ).exists()

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
        "user_liked": user_liked,
        "likes_count": post.likes.count(),
    }

    return render(
        request,
        "post_detail.html",
        context
    )


@login_required          
def post_create(request):

    if request.method == "POST":

        form = PostCreateForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            post.author = request.user
            post = form.save(commit=False)
            post.save()

            return redirect("post_list")

    else:
        form = PostCreateForm()

    return render(request,"post_create.html",{"form": form})


# @login_required
def post_update(request, slug):

    post = get_object_or_404(
        Post,
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
        return redirect("post_detail",slug=post.slug)

    else:

        form = PostUpdateForm(
            instance=post
        )

    return render(request,"post_update.html",{"form": form,"post": post})



@login_required
def post_delete(request, slug):

    post = get_object_or_404(Post,slug=slug)

    if request.method == "POST":
        author=request.user
        post.delete()

        return redirect("post_list")

    return render(request,"post_delete.html",{"post": post})
    

def search_posts(request):
    query=request.GET.get('q','')
    posts=Post.objects.all()
    if query:
        posts=posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) 
           ).distinct()
    
    context={'posts':posts, 'query': query, }
    return render(request, 'search_view.html',context)

def like_toggle(request,slug):
    post=get_object_or_404(Post,slug=slug)
    like,created=Likes.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
    return redirect('post_detail',slug=post.slug)

@login_required
def add_comment(requset,slug):
    post=get_object_or_404(Post,slug=slug)
    if requset.method=='POST':
        form=CommentForm(requset.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.author=requset.user
            comment.save()
    return redirect('post_detail',slug=post.slug)



    