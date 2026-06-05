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


class Ritsep(models.Model):

    author = models.ForeignKey(
        ControlUsers,
        on_delete=models.CASCADE,
        related_name="ritseps"
    )

    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        default="Ritsep nomi"
        
    )

    ritsep = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        default="Ritepni kiriting"
        
    )
    
    @property
    def average_rating(self):
        return self.ratings.aggregate(
        Avg("stars")
    )["stars__avg"] or 0


    images = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(
                f"{self.ritsep}-{str(uuid.uuid4())[:4]}"
            )

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "post_detail",
            kwargs={
                "slug": self.slug
            }
        )

    def __str__(self):
        return self.ritsep
    
class Comment(models.Model):
    ritsep = models.ForeignKey(
        Ritsep,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        ControlUsers,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.ritsep.name}"


class Rating(models.Model):
    ritsep = models.ForeignKey(
        Ritsep,
        on_delete=models.CASCADE,
        related_name="ratings"
    )

    user = models.ForeignKey(
        ControlUsers,
        on_delete=models.CASCADE
    )

    stars = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("ritsep", "user")

    def __str__(self):
        return f"{self.ritsep.name} - {self.stars}"