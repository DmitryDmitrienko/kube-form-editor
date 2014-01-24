#coding=UTF-8
__author__ = "Dmitry Dmitrienko"
__copyright__ = "Copyright 2014(c), Dmitry Dmitrienko"
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Dmitry Dmitrienko"
__email__ = "dmitry.dmitrienko@outlook.com"

from django import forms
from django.contrib.auth.models import User

from .models import FormModel


class FormForm(forms.ModelForm):
    class Meta:
        model = FormModel
        fields = ['name', 'description']


def get_users(user=None):
    if user is not None:
        users = User.objects.exclude(id=user.id).select_related('id', 'username')
    else:
        users = User.objects.select_related('id', 'username')
    return [(u.id, u.username) for u in users]


class FormChoiceUsers(forms.Form):
    users_for_share = forms.MultipleChoiceField(choices=get_users(), required=False)
    users_share = forms.MultipleChoiceField(choices=get_users(), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FormChoiceUsers, self).__init__(*args, **kwargs)
        if user:
            self.fields['users_for_share'].choices = get_users(user)
            self.fields['users_share'].choices = get_users(user)


class FormChoiceForm(forms.Form):
    forms = forms.ModelChoiceField(queryset=FormModel.objects.order_by('created'),
        widget=forms.Select(attrs={"onChange": 'submit()'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FormChoiceForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['forms'].queryset = FormModel.objects.filter(user=user).order_by('created')