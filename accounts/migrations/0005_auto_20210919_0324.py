# Generated by Django 3.1 on 2021-09-18 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userprofle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofle',
            name='profile_picture',
            field=models.ImageField(blank=True, default=None, upload_to='userprofile'),
        ),
    ]
