# Generated by Django 2.2.2 on 2019-07-23 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_bo_subscription_mapping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmaster',
            name='pro_status',
            field=models.IntegerField(null=True),
        ),
    ]
