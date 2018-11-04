import csv
import os

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from wagtail.images.models import Image

from blog.models import BlogPage, BlogIndexPage
from board.models import BoardPage
from contact.models import FormPage, ContactPage
from documents_gallery.models import DocumentsIndexPage, DocumentsPage
from events.models import EventPage, EventIndexPage
from membership.models import MembershipApplication
from pages.models import HomePage, StandardIndexPage, StandardPage, SiteBranding
from people.models import PersonPage, PersonIndexPage


class Command(BaseCommand):
    help = 'Create some default pages, remove some defaults'

    def handle(self, **options):
        # delete all the default content that we don't actually want
        PersonPage.objects.all().delete()
        PersonIndexPage.objects.all().delete()
        DocumentsPage.objects.all().delete()
        DocumentsIndexPage.objects.all().delete()
        EventPage.objects.all().delete()
        BlogPage.objects.all().delete()
        StandardIndexPage.objects.all().delete()
        StandardPage.objects.all().delete()

        # update some existing pages
        event_index = EventIndexPage.objects.filter().get()
        event_index.slug = 'events'
        event_index.title = 'Events'
        event_index.save()

        news_index = BlogIndexPage.objects.filter().get()
        news_index.slug = 'news'
        news_index.title = 'In the News'
        news_index.show_in_menus = False
        news_index.save()

        # set logo
        branding = SiteBranding.objects.filter().get()
        with open(os.path.join(settings.PROJECT_ROOT, 'media', 'original_images', 'grhs_logo.png'), 'rb') as f:
            logo_file = ImageFile(f, name='grhs_logo.jpg')
            logo = Image.objects.create(file=logo_file)
        branding.logo = logo
        branding.save()

        # add some new pages
        root_page = HomePage.objects.filter().get()

        about_us = StandardPage(title='About Us', slug='about-us', show_in_menus=True)
        root_page.add_child(instance=about_us)

        board = BoardPage(title='Board of Trustees', show_in_menus=True)
        about_us.add_child(instance=board)

        history_gr = StandardPage(title='History of GR', slug='history-of-gr', show_in_menus=True)
        root_page.add_child(instance=history_gr)

        support = StandardPage(title='Support', slug='support', show_in_menus=True)
        root_page.add_child(instance=support)

        membership = MembershipApplication(title='Membership', slug='membership', show_in_menus=True,
                                           thankyou_page_title='Thanks!')
        support.add_child(instance=membership)

        #donate = ...
        #support.add_child(instance=donate)

