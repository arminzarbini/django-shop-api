# Generated by Django 5.1.3 on 2024-12-03 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_rename_session_cart_session_key_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_amount',
            new_name='total_price',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='total_item',
            new_name='total_item_price',
        ),
    ]
