# Generated by Django 2.2.2 on 2019-07-20 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20190720_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='created_by',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='language',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='language',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='language',
            name='updated_by',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='language',
            name='user_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
