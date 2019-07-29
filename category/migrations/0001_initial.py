# Generated by Django 2.2.2 on 2019-07-19 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category_Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('category_description', models.CharField(max_length=250)),
                ('category_parent_id', models.IntegerField(null=True)),
                ('category_parent_child_id', models.CharField(max_length=1000, null=True)),
                ('category_created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('category_created_by', models.CharField(max_length=100, null=True)),
                ('category_updated_at', models.DateTimeField(null=True)),
                ('category_updated_by', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'category_master',
            },
        ),
        migrations.CreateModel(
            name='Filter_Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_name', models.CharField(max_length=100)),
                ('filter_status', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='category.Category_Master')),
            ],
            options={
                'db_table': 'filter_master',
            },
        ),
        migrations.CreateModel(
            name='Filter_Value_Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_value', models.CharField(max_length=100)),
                ('filter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='category.Filter_Master')),
            ],
            options={
                'db_table': 'filter_value_master',
            },
        ),
        migrations.CreateModel(
            name='Category_Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_image', models.ImageField(blank=True, upload_to='category')),
                ('category_featured_img', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.Category_Master')),
            ],
            options={
                'db_table': 'category_gallery',
            },
        ),
    ]
