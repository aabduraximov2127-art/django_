from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
import uuid


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi shart")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email,
            password,
            **extra_fields
        )


class ControlUsers(AbstractUser):

    username = None

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    age = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    email = models.EmailField(
        unique=True
    )

    phon = models.CharField(
        max_length=20,
        blank=True
    )

    avatar = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):

        if not self.slug:
            uid = str(uuid.uuid4())[:5]
    
            self.slug = slugify(
                f"{self.first_name}-{self.last_name}-{uid}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class UserProfile(models.Model):

    user = models.OneToOneField(
        ControlUsers,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    bio = models.TextField(blank=True)

    website = models.URLField(
        blank=True
    )

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=ControlUsers)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance
        )


@receiver(post_save, sender=ControlUsers)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    author = models.ForeignKey(ControlUsers,on_delete=models.CASCADE,related_name="posts")
    title = models.CharField(max_length=200)
    content = models.TextField()
    images = models.ImageField(upload_to="posts/",blank=True,null=True)
    view_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True,blank=True,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.title}-{str(uuid.uuid4())[:4]}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Likes(models.Model):
    user = models.ForeignKey(ControlUsers,on_delete=models.CASCADE,related_name="likes")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

class Meta:
    unique_together = ("user", "post")

def __str__(self):
    return f"{self.user.email} liked {self.post.title}"


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    author = models.ForeignKey(ControlUsers,on_delete=models.CASCADE,related_name="comments",null=True,blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Meta:
    ordering = ["-created_at"]

def __str__(self):

    if self.author:
        return f"{self.author.email} - {self.post.title}"

    return self.post.title

