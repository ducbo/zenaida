# Generated by Django 3.1.4 on 2020-12-19 14:51

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0015_auto_20190901_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='details',
            field=models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
    ]