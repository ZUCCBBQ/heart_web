# Generated by Django 2.1.8 on 2020-12-15 03:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detetction', '0005_users_create_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='user_id',
        ),
    ]