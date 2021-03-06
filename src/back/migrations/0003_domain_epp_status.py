# Generated by Django 2.1.5 on 2019-01-20 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0002_auto_20181119_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='epp_status',
            field=models.CharField(choices=[('EPP_STATUS_ACTIVE', 'ACTIVE'), ('EPP_STATUS_INACTIVE', 'INACTIVE'), ('EPP_STATUS_DEACTIVATED', 'DEACTIVATED'), ('EPP_STATUS_CLIENT_HOLD', 'CLIENT HOLD'), ('EPP_STATUS_SERVER_HOLD', 'SERVER HOLD'), ('EPP_STATUS_TO_BE_DELETED', 'TO BE DELETED'), ('EPP_STATUS_TO_BE_RESTORED', 'TO BE RESTORED'), ('EPP_STATUS_UNKNOWN', 'UNKNOWN(ERROR)')], default='INACTIVE', max_length=32),
        ),
    ]
