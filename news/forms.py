from django.contrib.auth.forms import UserCreationForm as user
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
class userForm(user):
    verify_code=forms.CharField(
        label=_("verify_code"),
        strip=False,
        widget=forms.TextInput,
    )
    email = forms.EmailField(label=_("Email"),max_length=254)