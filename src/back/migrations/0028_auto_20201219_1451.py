# Generated by Django 3.1.4 on 2020-12-19 14:51

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0027_auto_20200701_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='epp_statuses',
            field=models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
    ]