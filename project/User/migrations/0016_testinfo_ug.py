# Generated by Django 3.0.1 on 2020-12-07 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0015_remove_testinfo_ug'),
    ]

    operations = [
        migrations.AddField(
            model_name='testinfo',
            name='ug',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='User.testdata'),
        ),
    ]
