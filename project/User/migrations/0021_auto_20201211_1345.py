# Generated by Django 3.0.1 on 2020-12-11 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0020_boy_girl_love'),
    ]

    operations = [
        migrations.RenameField(
            model_name='girl',
            old_name='name',
            new_name='nick',
        ),
    ]