# Generated by Django 2.2.2 on 2019-07-21 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_auto_20190721_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter_master',
            name='filter_created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='filter_master',
            name='filter_created_by',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='filter_master',
            name='filter_updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='filter_master',
            name='filter_updated_by',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='filter_master',
            name='filter_user_type',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
