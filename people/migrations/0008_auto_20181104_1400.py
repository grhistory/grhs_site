# Generated by Django 2.1.2 on 2018-11-04 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0007_personpage_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personindexpage',
            name='subtitle',
            field=models.CharField(blank=True, help_text='This will override the title of the page.', max_length=255),
        ),
        migrations.AlterField(
            model_name='personpage',
            name='subtitle',
            field=models.CharField(blank=True, help_text='This will override the title of the page.', max_length=255),
        ),
    ]
