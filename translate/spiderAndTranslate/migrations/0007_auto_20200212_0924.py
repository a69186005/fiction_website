# Generated by Django 3.0.3 on 2020-02-11 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spiderAndTranslate', '0006_auto_20200211_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='originalbooks',
            name='book_category',
            field=models.TextField(default='', verbose_name='Book Category'),
        ),
    ]
