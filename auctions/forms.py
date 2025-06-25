from django import forms
from .models import Listings

class Create_Listing_form(forms.ModelForm):
    starting_bid = forms.FloatField(
        label='Starting Bid',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter the initial price'
        })
    )

    other_category = forms.CharField(
        required=False,
        label='Other (Specify)',
        widget=forms.TextInput(attrs={'placeholder': 'Specify other category'})
    )

    class Meta:
        model = Listings
        fields = ['title', 'description', 'imageUrl', 'starting_bid', 'category', 'other_category']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'imageUrl': 'Image URL',
            'category': 'Category',
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a short description about your listing...',
                'rows': 4
            }),
            'imageUrl': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/image.jpg'
            }),
        }
