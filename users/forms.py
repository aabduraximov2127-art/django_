from django import forms
from django.contrib.auth.forms import AuthenticationForm


from .models import ControlUsers,UserProfile,Post,Comment,Rating


class UserForm(forms.ModelForm):

    class Meta:
        model = ControlUsers

        fields = [
            "first_name",
            "last_name",
            "age",
            "email",
            "phon",
            "avatar"
        ]


class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput()
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = ControlUsers

        fields = [
            "first_name",
            "last_name",
            "age",
            "email",
            "phon",
            "avatar"
        ]

    def clean(self):
        cleaned_data = super().clean()

        if (
            cleaned_data.get("password1")
            !=
            cleaned_data.get("password2")
        ):
            raise forms.ValidationError(
                "Parollar mos emas"
            )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(
            commit=False
        )

        user.set_password(
            self.cleaned_data["password1"]
        )

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    pass


class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = [
            "bio",
            "website"
        ]


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = [
            "bio",
            "website"
        ]


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            'name',
            "ritsep",
            "images"
        ]


class PostUpdateForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            'name',
            'ritsep',
            "images"
        ]
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["stars"]