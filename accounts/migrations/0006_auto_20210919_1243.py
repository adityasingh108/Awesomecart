# Generated by Django 3.1 on 2021-09-19 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210919_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofle',
            name='address_line_1',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofle',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofle',
            name='city',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofle',
            name='country',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofle',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofle',
            name='state',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]