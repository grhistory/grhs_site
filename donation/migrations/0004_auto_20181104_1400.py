# Generated by Django 2.1.2 on 2018-11-04 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0003_donationpage_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationpage',
            name='subtitle',
            field=models.CharField(blank=True, help_text='This will override the title of the page.', max_length=255),
        ),
    ]
