from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel


class BoardMemberBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    role = blocks.CharBlock()
    joined_date = blocks.DateBlock()


class BoardPage(Page):
    description = RichTextField(blank=True)
    body = StreamField([
        ('board_members', blocks.ListBlock(BoardMemberBlock, label='Board Member',
                                           template='board/board_members.html'))
    ])

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        StreamFieldPanel('body')
    ]
