# Generated by Django 4.0 on 2023-05-07 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_user_debt'),
        ('book', '0004_bookinstance_date_borrow_alter_bookinstance_book_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debt', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
