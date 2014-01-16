from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from editor.models import FormModel


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
