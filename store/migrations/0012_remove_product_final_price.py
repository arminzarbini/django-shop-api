# Generated by Django 5.1.3 on 2024-12-05 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_product_final_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='final_price',
        ),
    ]