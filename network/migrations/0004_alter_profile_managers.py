# Generated by Django 4.0.1 on 2022-05-19 16:59

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_remove_profile_followers_profile_followers_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='profile',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]