# Generated by Django 2.1.2 on 2018-11-04 18:27

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0041_merge_20181104_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='show_announcement',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Special announcement text'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='title_text',
            field=wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Special announcement title'),
        ),
        migrations.AlterField(
            model_name='standardindexpage',
            name='template_string',
            field=models.CharField(choices=[('pages/standard_index_page.html', 'Child pages in sidebar'), ('pages/standard_page_full.html', 'Customized sidebar optional')], default='pages/standard_page_full.html', max_length=255, verbose_name='Page Layout'),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='template_string',
            field=models.CharField(choices=[('pages/standard_page_full.html', 'Optional custom sidebar'), ('pages/standard_page.html', 'Newsfeed sidebar')], default='pages/standard_page_full.html', max_length=255, verbose_name='Page Layout'),
        ),
    ]
