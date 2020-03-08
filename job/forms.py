from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import *
from django.forms import ModelChoiceField,ModelForm,TextInput,Textarea
from . choices import *
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
import datetime


# class CustomUserCreationForm(UserCreationForm):
#     username = forms.CharField(max_length=30,
#     widget=forms.TextInput)



class addJobForm(forms.Form):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), to_field_name="company",
    widget=forms.Select(attrs={'class':'form-control'}))


class CustomUserCreationFormCompany(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name','last_name','email','username')
        
    # def __init__(self, *args, **kwargs):
    #     super(CustomUserCreationFormDoctor, self).__init__(*args, **kwargs)
    #     self.fields['email'].label = "Email Address"
    #     self.fields['password1'].label = "Password"
    #     self.fields['password2'].label = "Re-Type Password"
    #     self.fields['dob'].label = "Date of Birth"

    @transaction.atomic    
    def save(self):        
        user = super().save(commit=False)
        user.is_company = True
        
        user.save()    
        company = Company.objects.create(user=user)  
            
        return company


class CustomUserCreationFormSeeker(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name','last_name','email','username')
        
    # def __init__(self, *args, **kwargs):
    #     super(CustomUserCreationFormDoctor, self).__init__(*args, **kwargs)
    #     self.fields['email'].label = "Email Address"
    #     self.fields['password1'].label = "Password"
    #     self.fields['password2'].label = "Re-Type Password"
    #     self.fields['dob'].label = "Date of Birth"

    @transaction.atomic    
    def save(self):        
        user = super().save(commit=False)
        user.is_seeker = True
        
        user.save()    
        seeker = Seeker.objects.create(user=user)  
            
        return seeker
