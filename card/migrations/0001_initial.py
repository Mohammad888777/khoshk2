# Generated by Django 5.0 on 2024-11-23 16:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0006_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, db_index=True, default=False, help_text='is active', null=True, verbose_name='is active')),
                ('card_id', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='created', verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, help_text='updated', verbose_name='updated')),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'cart',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(db_index=True, help_text='quantity', verbose_name='quantity')),
                ('is_active', models.BooleanField(blank=True, db_index=True, default=False, help_text='is_active', null=True, verbose_name='is_active')),
                ('cart_status', models.CharField(choices=[('paid', 'paid'), ('notPaid', 'notPaid')], default='notPaid', help_text='status', max_length=15, verbose_name='status')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, help_text='created', verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, help_text='updated', verbose_name='updated')),
                ('cart', models.ForeignKey(blank=True, help_text='cart', null=True, on_delete=django.db.models.deletion.CASCADE, to='card.cart', verbose_name='cart')),
                ('product', models.ForeignKey(blank=True, help_text='product', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.product', verbose_name='product')),
                ('user', models.ForeignKey(blank=True, help_text='user', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'cart item',
                'verbose_name_plural': 'cart item',
                'ordering': ['created'],
            },
        ),
    ]
