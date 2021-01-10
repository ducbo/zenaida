# Generated by Django 3.1.4 on 2021-01-10 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20201219_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='notes',
            field=models.TextField(blank=True, default=None, help_text='any note regarding this account such as manual balance changes.', null=True),
        ),
    ]
