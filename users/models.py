from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.text import slugify
import uuid
from django.urls import reverse


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email kiriting")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save() 

        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        return self.create_user(email, password, **kwargs)


class ControlUsers(AbstractUser):

    username=None
    age=models.PositiveIntegerField(default=14, blank=True, null=True)
    email=models.EmailField(unique=True)
    phon=models.CharField(max_length=20, blank=True)
    avatar=models.ImageField(upload_to="images/", blank=True, null=True)
    slug=models.SlugField(unique=True, blank=True)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]

    objects=CustomUserManager()

    def save(self, *args, **kwargs):

        if not self.slug:
            uid = str(uuid.uuid4())[:5]

            self.slug = slugify(
                f"{self.first_name}-{self.last_name}-{uid}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    
# profile
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(ControlUsers, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.user.email} profili"
    
@receiver(post_save, sender=ControlUsers)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    
@receiver(post_save, sender=ControlUsers)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Tag(models.Model):
    name=models.CharField(max_length=100, unique=True)
    slug=models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(ControlUsers, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=150)
    tags=models.ManyToManyField(Tag, blank=True,related_name='posts')
    content = models.TextField()
    images=models.ImageField(upload_to="post_images/", blank=True, null=True)
    craeted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    

    class Meta:
        ordering = ['-craeted_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{str(uuid.uuid4())[:4]}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        return f"{self.title}--{self.author.email}"