from django import forms
from django.contrib.auth.forms import AuthenticationForm
from . import models
from django.contrib.auth import get_user_model
from .models import Tag



class UserForm(forms.ModelForm):
    class Meta:
        model = models.ControlUsers
        fields = [
            'first_name',
            'last_name',
            'age',
            'email',
            'phon',
            'avatar'
        ]


class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Parol"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Parolni tasdiqlang"
        })
    )

    class Meta:
        model = models.ControlUsers
        fields = [
            'first_name',
            'last_name',
            'age',
            'email',
            'phon',
            'avatar'
        ]

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Parollar mos emas!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Email"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Parol"
        })
    )
# profile

class UserProfileUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input','placeholder': ' Ismingizni kiriting'}))
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input','placeholder': ' Familiyangizni kiriting'}))
    phon = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input','placeholder': ' Telefon raqamingizni kiriting'}))
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-input','placeholder': ' Rasm yuklang'}))
    email= forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input','placeholder': ' Email kiriting'}))
    bio=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input','placeholder': ' O\'z hususiyatlaringizni yozing'}))
    
    website=forms.URLField(widget=forms.URLInput(attrs={'class': 'form-input','placeholder': ' Vebsaytingizni kiriting'}))
    
    class Meta:
        model = models.UserProfile
        fields = [
            'first_name',
            'last_name',
            'phon',
            'avatar',
            'email',
            'bio',
            'website',
        ]
    
class ProfileDeleteForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = []
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = [
            'bio',
            'website',
        ]
        
        
class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Teglar"
    )

    class Meta:
        model=models.Post
        fields=['title', 'content', 'author', 'images', 'tags']
class PostCreateForm(forms.ModelForm):
    title=forms.CharField(max_length=200)
    content=forms.CharField(widget=forms.Textarea)
    images=forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = models.Post
        fields = [
            'title',
            'content',
            'images',
        ]
        
class PostUpdateForm(forms.ModelForm):
    title=forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-input','placeholder': ' Post sarlavhasini kiriting'}))
    content=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input','placeholder': ' Post mazmunini kiriting'}))
    images=forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-input','placeholder':
        ' Post uchun rasm yuklang'}))
    
    class Meta:
        model = models.Post
        fields = [
            'title',
            'content',
            'images',
        ]
class PostDeleteForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = []
class PostDetailForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = [
            'title',
            'content',
            'images',
        ]