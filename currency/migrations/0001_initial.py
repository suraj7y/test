# Generated by Django 2.2.2 on 2019-07-19 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=100)),
                ('currency_code', models.CharField(max_length=5)),
                ('country_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Country')),
            ],
            options={
                'db_table': 'currency_master',
            },
        ),
    ]
