from django import forms
from .models import Category


# Form for creating new listing
class NewListingForm(forms.Form):

    title = forms.CharField(label=False,
        widget=forms.TextInput(attrs={
            "autocomplete": "off", 
            "class": "form-control new_listing_form", 
            "placeholder": "Listing title"})
    )

    description = forms.CharField(label=False,
        widget=forms.Textarea(attrs={
            "autocomplete": "off", 
            "class": "form-control new_listing_form", 
            "placeholder": "Description"})
    )

    start_bid = forms.DecimalField(label=False,
        widget=forms.NumberInput(attrs={
            "autocomplete": "off", 
            "class": "form-control new_listing_form", 
            "placeholder": "Starting bid"})
    )

    cover = forms.CharField(label=False, required=False,
        widget=forms.TextInput(attrs={
            "autocomplete": "off", 
            "required": False,
            "class": "form-control new_listing_form", 
            "placeholder": "Image url"})
    )

    category = forms.ModelChoiceField(queryset=Category.objects.all(), label=False, required=False, empty_label="Choose a category",
        widget=forms.Select(attrs={
             "class":"form-control new_listing_form"})
    )


# Form for adding new category
class NewCategoryForm(forms.Form):

    name = forms.CharField(label=False,
        widget=forms.TextInput(attrs={
            "autocomplete": "off", 
            "class": "new_category", 
            "placeholder": "Type new category"})
    )


# Form for writing new comment
class NewCommentForm(forms.Form):

    headline = forms.CharField(label=False,
        widget=forms.TextInput(attrs={
            "autocomplete": "off", 
            "class": "new_comment_header", 
            "placeholder": "Type your headline here"})
    )

    text = forms.CharField(label=False,
        widget=forms.Textarea(attrs={
            "autocomplete": "off", 
            "class": "new_comment", 
            "placeholder": "Type your comment here"})
    )


# Form for placing new bid
class NewBidForm(forms.Form):
    
    amount = forms.DecimalField()
