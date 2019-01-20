# Generated by Django 2.1.5 on 2019-01-20 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='merchant_reference',
            field=models.CharField(blank=True, default=None, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='started_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('started', 'Started'), ('failed', 'Failed'), ('paid', 'Paid'), ('processed', 'Processed')], default='started', max_length=16),
        ),
        migrations.AlterField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]
