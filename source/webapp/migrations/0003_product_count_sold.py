# Generated by Django 3.1.4 on 2021-07-18 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20210718_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='count_sold',
            field=models.IntegerField(default=0, verbose_name='Кол-во проданных'),
        ),
    ]
