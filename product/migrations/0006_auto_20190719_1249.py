# Generated by Django 2.2.2 on 2019-07-19 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20190719_0528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmaster',
            name='pro_bo_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='pro_brand',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='productmaster',
            name='pro_cat_id',
            field=models.IntegerField(null=True),
        ),
    ]
