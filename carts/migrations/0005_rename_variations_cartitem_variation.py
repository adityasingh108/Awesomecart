# Generated by Django 3.2.3 on 2021-09-09 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_rename_variation_cartitem_variations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='variations',
            new_name='variation',
        ),
    ]