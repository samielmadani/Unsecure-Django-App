from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import FileInput
from django.utils.html import strip_tags


from authentication.models import UserProfile, UserAddress
from main.models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "What's on your mind?"}), max_length=1000, help_text="1000 characters max.")
    image = forms.ImageField(widget=FileInput, required=False)

    class Meta:
        model = Post
        fields = ('text', 'image')


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••••••••••"}),
    )
    new_password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••••••••••"}),
    )
    new_password2 = forms.CharField(
        label="Password Check",
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••••••••••"}),
    )


class EditProfileForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        max_length=1000,
        widget=CKEditorWidget(attrs={"placeholder": "Tell us more about you"}),
    )
    
    profile_image = forms.ImageField(widget=forms.ClearableFileInput, required=False)
    cover_image = forms.ImageField(widget=forms.ClearableFileInput, required=False)

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        stripped = strip_tags(bio)
        return "<p>" + stripped + "</p>"

    class Meta:
        model = UserProfile
        fields = ["bio", "profile_image", "cover_image"]


class EditAddressForm(forms.ModelForm):
    country = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={}),
    )
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={}),
    )
    street = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={}),
    )
    postcode = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={}),
    )

    class Meta:
        model = UserAddress
        fields = ["country", "city", "street", "postcode"]
