# Generated by Django 2.2.2 on 2019-07-22 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20190720_0623'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bo_subscription_mapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_ownerid', models.IntegerField(null=True)),
                ('subscriptionid', models.CharField(max_length=250, null=True)),
                ('subcription_start_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('subcription_end_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'bo_subscription_mapping',
            },
        ),
    ]
