# Generated by Django 4.0 on 2023-05-02 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='debt',
            field=models.IntegerField(default=0),
        ),
    ]
