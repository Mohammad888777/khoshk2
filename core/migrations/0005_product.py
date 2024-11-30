# Generated by Django 5.0 on 2024-11-21 09:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_firstslider_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text='is_active', verbose_name='is_active')),
                ('name', models.CharField(db_index=True, help_text='name', max_length=100, verbose_name='name')),
                ('image', models.ImageField(blank=True, db_index=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])),
                ('description', models.TextField(blank=True, db_column='description', db_index=True, help_text='description', null=True, verbose_name='description')),
                ('price', models.PositiveIntegerField(blank=True, db_index=True, help_text='price', null=True, verbose_name='price')),
                ('stock_number', models.PositiveIntegerField(blank=True, db_index=True, help_text='stock kilogramm', null=True, verbose_name='stock kilogramm')),
                ('in_stock', models.BooleanField(blank=True, db_index=True, default=True, help_text='in stock', null=True, verbose_name='in stock')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='created time', verbose_name='created time')),
                ('updated', models.DateTimeField(auto_now=True, db_column='updated', db_index=True, help_text='updated time', verbose_name='updated time')),
            ],
        ),
    ]
