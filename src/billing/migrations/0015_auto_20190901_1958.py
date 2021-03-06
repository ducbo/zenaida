# Generated by Django 2.2.4 on 2019-09-01 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0014_auto_20190811_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('started', 'Started'), ('processing', 'Processing'), ('cancelled', 'Cancelled'), ('failed', 'Failed'), ('incomplete', 'Incomplete'), ('processed', 'Processed')], default='started', max_length=16),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('started', 'Started'), ('pending', 'Pending'), ('failed', 'Failed'), ('processed', 'Processed')], default='started', max_length=16),
        ),
    ]
