# Generated by Django 3.0.1 on 2020-12-16 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0029_auto_20201216_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='c_time',
            field=models.DateTimeField(null=True),
        ),
    ]
