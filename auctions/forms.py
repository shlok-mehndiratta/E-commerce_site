from django import forms
from .models import Category, Listings

class Create_Listing_form(forms.ModelForm):
    other_category = forms.CharField(
        required=False,
        label='Other (Specify)',
        widget=forms.TextInput(attrs={'placeholder': 'Specify other category'})
    )

    class Meta:
        model = Listings
        fields = ['title', 'description', 'price', 'imageUrl', 'category', 'other_category']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'price': 'Starting Bid',
            'imageUrl': 'Image url',
            'category': 'Category',
        }
        widgets = {
            'description': forms.Textarea(),
        }

