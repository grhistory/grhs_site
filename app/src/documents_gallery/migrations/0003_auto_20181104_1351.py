# Generated by Django 2.1.2 on 2018-11-04 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents_gallery', '0002_auto_20180607_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentsindexpage',
            name='subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='documentspage',
            name='subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]