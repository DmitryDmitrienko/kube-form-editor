#coding=UTF-8
__author__ = "Dmitry Dmitrienko"
__copyright__ = "Copyright 2014(c), Dmitry Dmitrienko"
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Dmitry Dmitrienko"
__email__ = "dmitry.dmitrienko@outlook.com"

from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.models import Permission

from .models import FormModel


class FormForm(forms.ModelForm):
    class Meta:
        model = FormModel
        fields = ['name', 'description']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']



def get_users(user=None, form=None):
    if user is not None and form is not None:
        try:
            permissions = Permission.objects.filter(
                codename__icontains="can_edit_%s_%s" % (form.id, form.name)).select_related('codename')
            user_list = [
                p.codename.split('_')[0]
                for p in permissions
            ]
            u_p = [(u.id, u.username) for u in User.objects.exclude(id=user.id).filter(username__in=user_list)]
            u = [(u.id, u.username) for u in User.objects.exclude(username__in=user_list).exclude(id=user.id)]
            return u_p, u
        except Exception as e:
            print e.message
            return [], []
    else:
        return [], []


class FormChoiceUsers(forms.Form):
    users_for_share = forms.MultipleChoiceField(choices=get_users(), required=False)
    users_share = forms.MultipleChoiceField(choices=get_users(), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        form = kwargs.pop('form', None)
        super(FormChoiceUsers, self).__init__(*args, **kwargs)
        if user and form:
            u_p, u = get_users(user, form)
            self.fields['users_for_share'].choices = u
            self.fields['users_share'].choices = u_p


class FormChoiceForm(forms.Form):
    forms = forms.ModelChoiceField(queryset=FormModel.objects.order_by('created'),
                                   widget=forms.Select(attrs={"onChange": 'submit()'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FormChoiceForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['forms'].queryset = FormModel.objects.filter(user=user).order_by('created')