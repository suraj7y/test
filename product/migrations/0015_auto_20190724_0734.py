# Generated by Django 2.2.2 on 2019-07-24 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_auto_20190724_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='featured_image',
            field=models.BooleanField(default=False),
        ),
    ]
