#coding=UTF-8
__author__ = "Dmitry Dmitrienko"
__copyright__ = "Copyright 2014(c), Dmitry Dmitrienko"
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Dmitry Dmitrienko"
__email__ = "dmitry.dmitrienko@outlook.com"

from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import auth_login, logout_then_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from editorform.settings import LOGIN_URL
from editor.models import FormModel
from editor.forms import FormForm, FormChoiceUsers, FormChoiceForm


def str_permission(user_name, form_id, form_name):
    return "%s_can_edit_%s_%s" % (user_name, form_id, form_name)


class PermissionsRequiredMixin(object):
    object_form = None

    def get_object_form(self, **kwargs):
        if 'form_id' in kwargs:
            f = FormModel.objects.get(id=kwargs['form_id'])
            self.object_form = f
        return self.object_form

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object_form(**kwargs)
        if obj is not None:
            str = "editor." + str_permission(request.user.username, obj.id, obj.name)
            if request.user.is_superuser is False and request.user.has_perm(str):
                messages.success(
                    request,
                    u'Расшаренная форма')
                return super(PermissionsRequiredMixin, self).dispatch(request, *args, **kwargs)
            elif obj.user != request.user:
                messages.error(
                    request,
                    u'Доступ к не разрешенной форме')
                return redirect(reverse('index'))
        return super(PermissionsRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class AuthenticateView(FormView):
    form_class = AuthenticationForm
    template_name = "authenticate.html"
    http_method_names = ('post', 'get', )

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if self.request.GET:
            return redirect(self.request.GET['next'])
        else:
            return super(AuthenticateView, self).form_valid(form)


def logout(request):
    return logout_then_login(request, login_url='/login')


class CreateUserView(FormView):
    form_class = UserCreationForm
    template_name = 'createuser.html'

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        user = form.save()
        f = super(CreateUserView, self).form_valid(form)
        return f


class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        u = self.request.user
        if not u.is_anonymous():
            context.update({
                'forms': FormModel.objects.filter(user=self.request.user).select_related('id', 'name', 'description')
            })
        return context


class CreateFormView(CreateView):
    template_name = "createform.html"
    form_class = FormForm
    model = FormModel

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        u = self.request.user
        if not u.is_anonymous():
            data = form.cleaned_data
            data.update({
                'user': self.request.user
            })
            self.object = self.model(**data)
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(CreateFormView, self).form_invalid(form)


class UpdateFormView(PermissionsRequiredMixin, UpdateView):
    template_name = "updateform.html"
    form_class = FormForm
    model = FormModel
    pk_url_kwarg = 'form_id'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse('index')


class DeleteFormView(PermissionsRequiredMixin, DeleteView):
    template_name = "deleteform.html"
    model = FormModel
    pk_url_kwarg = "form_id"
    context_object_name = "form"

    def get_success_url(self):
        return reverse('index')


class ShareView(PermissionsRequiredMixin, FormView):
    template_name = "share.html"
    form_class = FormChoiceUsers

    def get_success_url(self):
        return reverse('share', args=(self.kwargs['form_id'],))

    def form_valid(self, form):
        context = self.get_context_data(**self.kwargs)
        f = FormModel.objects.get(id=context['form_id'])
        data = form.cleaned_data
        if 'share_to' in form.data:
            ShareView.create_permission(data['users_for_share'], f.id, f.name)
        elif 'share_delete' in form.data:
            ShareView.delete_permission(data['users_share'], f.id, f.name)
        return super(ShareView, self).form_valid(form)

    @staticmethod
    def create_permission(user_list, form_id, form_name):
        content_type = ContentType.objects.get_for_model(FormModel)
        for user in user_list:
            try:
                u = User.objects.get(id=user)
                s = str_permission(u.username, form_id, form_name)
                title = "%s can edit %s %s" % (u.username, form_id, form_name)
                permission = Permission.objects.create(codename=s,
                                                       name=title,
                                                       content_type=content_type)
                u.user_permissions.add(permission)
            except Exception as e:
                print e.message

    @staticmethod
    def delete_permission(user_list, form_id, form_name):
        for user in user_list:
            try:
                u = User.objects.get(id=user)
                content_type = ContentType.objects.get_for_model(FormModel)
                p = Permission.objects.get(codename=str_permission(u.username, form_id, form_name),
                                           content_type=content_type)
                u.user_permissions.remove(p)
                p.delete()
            except Exception as e:
                print e.message


    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
            'form': FormModel.objects.get(id=self.kwargs['form_id'])
        })
        return self.form_class(**kwargs)


class FormView(PermissionsRequiredMixin, FormView):
    template_name = "formview.html"
    form_class = FormChoiceForm
    object = None

    def get_object(self):
        return self.object

    def get_initial(self):
        init = self.initial.copy()
        data = self.get_context_data(**self.kwargs)
        if 'form_id' in data:
            init.update({
                'forms': FormModel.objects.get(id=data['form_id'])
            })
        return init

    def form_valid(self, form):
        data = form.data
        self.success_url = reverse('form', args=(data['forms'], ))
        return super(FormView, self).form_valid(form)

    def get_form(self, form_class):
        kwargs = self.get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return self.form_class(**kwargs)
