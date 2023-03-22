from django import forms
from django.contrib.auth.models import User
from .models import Message, Profile

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'name', 'description', 'website', 'email']

    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != self.instance.user.email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

