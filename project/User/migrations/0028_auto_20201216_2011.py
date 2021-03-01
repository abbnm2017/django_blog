# Generated by Django 3.0.1 on 2020-12-16 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0027_remove_boy_m'),
    ]

    operations = [
        migrations.AddField(
            model_name='boy',
            name='m',
            field=models.ManyToManyField(through='User.Love', to='User.Girl'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='f',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
