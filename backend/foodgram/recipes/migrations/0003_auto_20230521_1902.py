# Generated by Django 2.2.16 on 2023-05-21 13:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_auto_20230519_1223'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Purchase',
            new_name='ShoppingCart',
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
