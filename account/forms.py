from django import forms
from django.core.mail import send_mail
from account.models import User


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name', 'image')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('User with given username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with given email already exists')
        return email


    def save(self, commit=True):
        user = User.objects.create(**self.cleaned_data)
        password = User.objects.make_random_password(length=8)
        user.set_password(password)
        user.save()

        send_mail(
            'From library site',
            f'Your password for the {user.username} account is: {password}',
            'librarynazsar@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return user
