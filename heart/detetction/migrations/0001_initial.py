# Generated by Django 2.1.8 on 2020-12-09 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('user_id', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='user_id')),
                ('name', models.CharField(max_length=15, verbose_name='name')),
                ('mails', models.EmailField(max_length=254, verbose_name='mails')),
                ('password', models.CharField(max_length=15, verbose_name='password')),
                ('reason', models.TextField(max_length=100, verbose_name='reason')),
            ],
        ),
    ]
