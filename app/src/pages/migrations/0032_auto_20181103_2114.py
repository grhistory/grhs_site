# Generated by Django 2.1.2 on 2018-11-03 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0031_auto_20181103_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awardpage',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
