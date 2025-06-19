from django import forms
from .models import Category


class Create_Listing_form(forms.Form):
    title = forms.CharField(label='Title')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price = forms.DecimalField(label='Starting Bid')
    imageUrl = forms.ImageField(label="Image url", required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category', required=False)
    other_category = forms.CharField(required=False, label='Other (Specify)', widget=forms.TextInput(attrs={'placeholder': 'Specify other category'}))
