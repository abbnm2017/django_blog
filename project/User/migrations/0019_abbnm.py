# Generated by Django 3.0.1 on 2020-12-08 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0018_testdata_testinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='abbnm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md', models.IntegerField(default=1)),
            ],
        ),
    ]