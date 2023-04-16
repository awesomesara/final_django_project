# Generated by Django 4.0 on 2023-04-15 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=100, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('activation_code', models.CharField(blank=True, max_length=15)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
