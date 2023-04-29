from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from account.forms import RegistrationForm
from account.models import User
from book.models import Borrower


class RegisterView(CreateView, SuccessMessageMixin):
    model = User
    template_name = 'account/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    success_message = 'Successfully registered'

    def form_valid(self, form):
        password = User.objects.make_random_password()
        user = form.save(commit=False)
        user.set_password(password)
        user.save()

        borrower = Borrower(user=user)
        borrower.save()

        send_mail(
            'From library site',
            f'Your passwords for {user.username} account: {password}',
            'forshipingsara@gmail.com',
            [user.email],
        )
        response = User.form_valid(form)
        return response


class SingInView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('home')

    def profile(request):
        return render(request, 'account/profile.html')


def profile(request):
    return render(request, 'account/profile.html')



