from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.forms import ModelForm, TextInput, NumberInput, EmailInput, PasswordInput, Select, FileInput
from .models import UserProfile
from django.forms import ModelForm



class SignupForm(UserCreationForm):
    username=forms.CharField(max_length=50, label="username",widget=forms.TextInput(
        attrs={'placeholder':"Write your username",}
    ))
    email=forms.EmailField(max_length=200, label="email",widget=forms.EmailInput(
        attrs={'placeholder':"Write your email",}
    ))
    first_name=forms.CharField(max_length=30, label="first name",widget=forms.TextInput(
        attrs={'placeholder':"Write your first name",}
    ))
    last_name=forms.CharField(max_length=30, label="last name",widget=forms.TextInput(
        attrs={'placeholder':"Write your last name",}
    ))
    
    
    
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password1','password2',]
        widgets={
            'password1':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter a new Password'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm your Password'}),
            

        }


class UserUpdateForm(UserChangeForm):
    class Meta:
        model=User
        fields=('username','email','first_name','last_name')
        widgets={
            'username':TextInput(attrs={'class':'input','placeholder':'username'}),
            'email':EmailInput(attrs={'class':'input','placeholder':'email'}),
            'first_name':TextInput(attrs={'class':'input','placeholder':'first_name'}),
            'last_name':TextInput(attrs={'class':'input','placeholder':'last_name'}),
        }


CITY = [
    ('Dhaka', 'Dhaka'),
    ('Mymensign', 'Mymensign'),
    ('Rajshahi', 'Rajshahi'),
    ('Rangpur', 'Rangpur'),
    ('Barisal', 'Barisal'),
    ('Chottogram', 'Chottogram'),
    ('Khulna', 'Khulna'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'phone'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'address'}),
            'city': Select(attrs={'class': 'input', 'placeholder': 'city'}, choices=CITY),
            'country': TextInput(attrs={'class': 'input', 'placeholder': 'country'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }
