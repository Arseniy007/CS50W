from django import forms

# Form for searching new page
class SearchForm(forms.Form):

    query = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={"placeholder": "Search entry", "autocomplete": "off"})
        )

# Form for creating new wiki page
class NewPageForm(forms.Form):

    title = forms.CharField(
        label="Title of the page"
        )

    content = forms.CharField(
        label=False,
        widget=forms.Textarea
        )
    
# Form for editing an existing wiki page
class EditForm(forms.Form):

    title = forms.CharField(
        required=False,
        widget=forms.HiddenInput
    )

    content = forms.CharField(
        widget= forms.Textarea

    )