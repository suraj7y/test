# Generated by Django 2.2.2 on 2019-07-24 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20190724_0657'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationcode',
            name='verification_status',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
