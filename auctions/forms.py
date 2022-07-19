from django import forms 
from .models import Listing

class ListingForm(forms.ModelForm):
    model = Listing 
    fields = ('title', 'description', 'starting_price', 'image', 'category')