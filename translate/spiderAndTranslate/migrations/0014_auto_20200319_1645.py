# Generated by Django 3.0.3 on 2020-03-19 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spiderAndTranslate', '0013_auto_20200318_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tanslationbookcontenten',
            name='chapter_name',
            field=models.TextField(default='', verbose_name='Chapter Name'),
        ),
        migrations.AlterField(
            model_name='tanslationbookcontentvi',
            name='chapter_name',
            field=models.TextField(default='', verbose_name='Chapter Name'),
        ),
    ]
