from django import forms 
from .models import Listing, Bid 

class ListingForm(forms.ModelForm):
    class Meta:
       model = Listing 
       fields = ('title', 'description', 'starting_price', 'image', 'category')

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid 
        fields = ('price',)
        labels = {
        "price": "Enter Your Bid"
    }
