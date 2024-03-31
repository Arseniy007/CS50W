from django import forms


class NewPostForm(forms.Form):

    text = forms.CharField(label=False, 
        widget= forms.Textarea(attrs={
            "autocomplete": "off",
            "class": "form-control form-control-sm",
            "id": "new_post"
        }))
