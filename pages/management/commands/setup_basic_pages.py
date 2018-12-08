import csv
import os
import json

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from wagtail.images.models import Image

from blog.models import BlogPage, BlogIndexPage
from board.models import BoardPage, BoardMemberBlock
from contact.models import FormPage, ContactPage
from documents_gallery.models import DocumentsIndexPage, DocumentsPage
from donation.models import DonationPage
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
        event_pages = self.create_events_from_csv()
        for page in event_pages:
            event_index.add_child(instance=page)

        event_index.save()

        news_index = BlogIndexPage.objects.filter().get()
        news_index.slug = 'news'
        news_index.title = 'In the News'
        news_index.show_in_menus = False
        news_index.save()

        contact = ContactPage.objects.filter().get()
        contact.title = 'Contact'
        contact.save()

        # set logo
        branding = SiteBranding.objects.filter().get()
        with open(os.path.join(settings.PROJECT_ROOT, 'media', 'original_images', 'grhs_logo.png'), 'rb') as f:
            logo_file = ImageFile(f, name='grhs_logo.jpg')
            logo = Image.objects.create(file=logo_file)
        branding.logo = logo
        branding.save()

        # add some new pages
        root_page = HomePage.objects.filter().get()
        root_page.show_in_menus = False
        root_page.save()

        about_us = StandardIndexPage(template_string='pages/standard_index_page.html',
                                     title='About', slug='about', show_in_menus=True)
        root_page.add_child(instance=about_us)

        board_members = self.get_board_members()
        board = BoardPage(title='Board of Trustees',
                          body=json.dumps([
                                {'type': 'board_members', 'value': board_members}
                          ]),
                          show_in_menus=True)
        about_us.add_child(instance=board)

        history_gr = StandardPage(title='GR History', slug='history', show_in_menus=True)
        root_page.add_child(instance=history_gr)

        donate = DonationPage(title='Donate', slug='donate', show_in_menus=True)
        root_page.add_child(instance=donate)

        join = MembershipApplication(title='Join', slug='membership', show_in_menus=True,
                                           thankyou_page_title='Thanks!')
        root_page.add_child(instance=join)

    def get_board_members(self):
        board_members_csv = os.path.join(settings.PROJECT_ROOT, 'data', 'grhistorysociety_board.csv')

        board_members_list = []
        with open(board_members_csv, 'r') as f:
            board_members = csv.DictReader(f)
            for member in board_members:
                # The fields we add here need to match the fields on BoardMemberBlock, or else it will fail silently :(
                board_members_list.append({
                    'name': member['name'],
                    'role': member['position']
                })

        return board_members_list

    def create_events_from_csv(self):
        events_csv = os.path.join(settings.PROJECT_ROOT, 'data', 'grhistorysociety_event.csv')
        event_images_directory = os.path.join(settings.PROJECT_ROOT, 'data', 'event-images')

        event_pages = []
        with open(events_csv, 'r') as f:
            events = csv.DictReader(f)
            for event in events:
                dates = event['dates'].split(',')
                if len(dates) == 2:
                    date_from = dates[0]
                    date_to = dates[1]
                else:
                    # just assume this will work, csv shouldn't change so shouldn't be an issue
                    date_from = dates[0]
                    date_to = None

                image = self.get_event_image(event_images_directory, event['image'])

                e = EventPage(
                    title=event['title'],
                    time_from=event['time'] if event['time'] else None,
                    location=event['address'],
                    body=event['description'],
                    date_from=date_from,
                    date_to=date_to,
                    feed_image=image
                )
                e.tags.add(event['category'])
                event_pages.append(e)

        return event_pages

    def get_event_image(self, event_images_directory, image_name):
        try:
            with open( os.path.join(event_images_directory, image_name) , 'rb') as f:
                image_file = ImageFile(f, name=image_name)
                image = Image.objects.create(file=image_file)
                return image
        except (FileNotFoundError, IsADirectoryError):
            return None
