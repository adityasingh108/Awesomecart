# Generated by Django 3.1 on 2021-09-19 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210919_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofle',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='userprofile'),
        ),
    ]
