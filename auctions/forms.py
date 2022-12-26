from email.policy import default
from django import forms 

from .models import Category


class CreateForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200, required=True)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=20, decimal_places=2, required=True)

    image = forms.URLField(required=False)


    CATEGORY_CHOICES = [(cat.code, cat.description) for cat in Category.objects.all()]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)