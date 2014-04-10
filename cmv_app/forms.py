from django import forms
from cmv_app.models import Search
#from .models import UserProfile


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        exclude = ("user", "created",)
        
        

# #not implemented yet
# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         exclude = ("user",)

