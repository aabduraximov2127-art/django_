from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm

urlpatterns = [

    path("", views.home, name="home"),
    path("create/", views.user_create, name="user_create"),
    path("update/<slug:slug>/", views.user_update, name="user_update"),
    path("delete/<int:id>/", views.user_delete, name="user_delete"),
    path('user/<slug:slug>/', views.user_detail, name='user_detail'),
    path("register/", views.register_view, name="register_view"),
    path("login/",views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('users/', views.user_list, name='user_list'),
    path('profile/<slug:slug>/', views.profile, name='profile'),
    path('profile/update/<slug:slug>/', views.profile_update, name='profile_update'),
    path('profile/delete/<slug:slug>/', views.profile_delete, name='profile_delete'),
    # path('userprofile/update/<slug:slug>/', views.userprofile_update, name='userprofile_update'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('posts/<slug:slug>/update/', views.post_update, name='post_update'),
    path('posts/<slug:slug>/delete/', views.post_delete, name='post_delete'),

    ]