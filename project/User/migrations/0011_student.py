# Generated by Django 3.0.1 on 2020-09-22 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0010_auto_20200830_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('classes', models.CharField(max_length=100)),
            ],
        ),
    ]
