from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

# Register/Create a user 

class CreateUserForm(UserCreationForm):
    # Adding the profession field
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','username', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        # Make first_name and last_name required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("First name is required.")
        if any(char.isdigit() for char in first_name):  # Check for numeric characters
            raise forms.ValidationError("First name cannot contain numeric data.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("Last name is required.")
        if any(char.isdigit() for char in last_name):  # Check for numeric characters
            raise forms.ValidationError("Last name cannot contain numeric data.")
        return last_name



# login a user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# class Questionnaire(forms.Form):
#     user_investment = forms.ChoiceField

