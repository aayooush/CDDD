from django import forms


class Newform(forms.Form):
    image = forms.ImageField()