# Generated by Django 3.1.4 on 2021-07-19 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_product_discounted_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images', verbose_name='Изображение'),
        ),
    ]
