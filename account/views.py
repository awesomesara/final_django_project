from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from account.forms import RegistrationForm
from account.models import User


class RegisterView(CreateView, SuccessMessageMixin,FormView):
    model = User
    template_name = 'account/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    success_message = 'Successfully registered'


class SingInView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('home')

    def profile(request):
        return render(request, 'account/profile.html')


def profile(request):
    return render(request, 'account/profile.html')



