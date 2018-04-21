from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.core.validators import validate_comma_separated_integer_list
from accounts.models import UserProfile,User


CHOICES=[
    ('free','Free'),
    ('gold','Gold'),
    ('platinum','Platinum')
]


class ProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=(
            'description',
            'city',
            'website',
            'phone'
        )


class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    usertype=forms.ChoiceField(choices=CHOICES)

    class Meta:
        model=User
        fields=(
            'email',
            'usertype',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user=super(RegistrationForm,self).save(commit=False)
        user.usertype = self.cleaned_data['usertype']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):

    class Meta:
        model=User
        fields=(
            'email',
            'password'
        )


class Calc(forms.Form):
    tup=forms.CharField(validators=[validate_comma_separated_integer_list],label="Enter Values between 0 and 10 only separated by comma",required=True)