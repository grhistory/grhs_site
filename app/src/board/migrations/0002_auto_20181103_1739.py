# Generated by Django 2.1.2 on 2018-11-03 17:39

import board.models
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardpage',
            name='body',
            field=wagtail.core.fields.StreamField([('board_members', wagtail.core.blocks.ListBlock(board.models.BoardMemberBlock, label='Board Member', template='board/board_members.html'))]),
        ),
    ]
