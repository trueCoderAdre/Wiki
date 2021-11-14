from django import forms
from django.forms.widgets import HiddenInput
from . import util


class CreateNewPageForm(forms.Form):
    name_page = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)


class EditArticle(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    title = forms.CharField(widget=forms.HiddenInput())

