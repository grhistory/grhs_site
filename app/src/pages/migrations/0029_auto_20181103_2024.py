# Generated by Django 2.1.2 on 2018-11-03 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0028_auto_20181103_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awardpage',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
