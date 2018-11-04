import csv
import os

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from wagtail.images.models import Image


from pages.models import AwardPage, AwardIndexPage, HomePage

DEFAULT_AWARD_TITLE = 'Baxter Awards'
DEFAULT_DESCRIPTION = """
The Baxter Award was created in 1980 by the society to honor persons who have made significant contributions to the preservation and interpretation of Grand River Valley history. Named in honor of Albert Baxter, one of Grand Rapids early historians who published, History of the City of Grand Rapids, Michigan in 1891.

2018 marks 38 years of honoring these great men and women. Thank you! — GRHS
"""


class Command(BaseCommand):
    help = 'Create Baxter Award Pages'

    def handle(self, **options):
        baxter_images = os.path.join(settings.PROJECT_ROOT, 'pages', 'media', 'baxter-winner-photos')
        data_src = os.path.join(settings.PROJECT_ROOT, 'data')

        AwardIndexPage.objects.all().delete()
        root_page = HomePage.objects.filter().get()

        index_page = AwardIndexPage(title=DEFAULT_AWARD_TITLE, description=DEFAULT_DESCRIPTION, show_in_menus=True)
        root_page.add_child(instance=index_page)
        index_page.save_revision().publish()

        image_files_dict = {filename.split('.')[0]: os.path.join(baxter_images, filename)
                            for filename in os.listdir(baxter_images)}

        with open(os.path.join(data_src, 'grhistorysociety_baxter_award.csv')) as csvfile:
            past_winners_reader = csv.DictReader(csvfile)
            for row in past_winners_reader:
                year = row.get('year')
                if year in image_files_dict:
                    with open(image_files_dict[year], 'rb') as f:
                        image_file = ImageFile(f, name='{}_winner_photo.jpg'.format(year))
                        image = Image.objects.create(file=image_file)
                else:
                    image = None

                page = AwardPage(title='{year} {award_title}'.format(year=year, award_title=DEFAULT_AWARD_TITLE),
                                 winner=row.get('name'),
                                 year=row.get('year'),
                                 body=row.get('description'),
                                 image=image)
                index_page.add_child(instance=page)

        index_page.save_revision().publish()
