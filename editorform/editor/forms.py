#coding=UTF-8
__author__ = "Dmitry Dmitrienko"
__copyright__ = "Copyright 2014(c), Dmitry Dmitrienko"
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Dmitry Dmitrienko"
__email__ = "dmitry.dmitrienko@outlook.com"

from django import forms
from .models import FormModel


class CreateForm(forms.ModelForm):
    class Meta:
        model = FormModel
        fields = ['name', 'description']