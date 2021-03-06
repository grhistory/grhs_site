# Generated by Django 2.1.2 on 2018-11-03 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('pages', '0027_auto_20181103_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='awardpagegalleryimage',
            name='image',
        ),
        migrations.RemoveField(
            model_name='awardpagegalleryimage',
            name='page',
        ),
        migrations.RemoveField(
            model_name='awardpage',
            name='date_awarded',
        ),
        migrations.AddField(
            model_name='awardpage',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='awardpage',
            name='year',
            field=models.IntegerField(default=2018),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='AwardPageGalleryImage',
        ),
    ]
