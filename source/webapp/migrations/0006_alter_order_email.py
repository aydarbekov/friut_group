# Generated by Django 3.2.6 on 2021-08-10 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, verbose_name='Email'),
        ),
    ]
