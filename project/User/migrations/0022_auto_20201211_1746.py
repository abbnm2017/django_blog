# Generated by Django 3.0.1 on 2020-12-11 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0021_auto_20201211_1345'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='love',
            unique_together={('b', 'g')},
        ),
    ]
