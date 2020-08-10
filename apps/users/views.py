from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import FormView, TemplateView, RedirectView
from django.urls import reverse_lazy

# Create your views here.
from django.views.generic.base import View

from apps.users.forms import RegisterForm, ConfForm

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:profile')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog_home_work:index')


class LogoutView(RedirectView):
    pattern_name = 'blog_home_work:index'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'contents/author.html'


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:confirm')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.s_key()
        user.save()
        user.email_user('Подтверждение регистрации', str(user.secret_key))
        login(self.request, user)
        return super().form_valid(form)


class ConfirmView(FormView):
    template_name = 'users/confirm.html'
    form_class = ConfForm
    success_url = reverse_lazy('blog_home_work:index')

    def form_valid(self, form):
        u = form.save(commit=False)
        fff = self.request.POST.get('secret_key')
        u = self.request.user
        if u.secret_key == fff:
            u.confirm = True
            print(u.confirm)
        u.save()
        login(self.request, u)
        return super().form_valid(form)
