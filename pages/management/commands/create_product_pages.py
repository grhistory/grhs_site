import csv
import os

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from wagtail.images.models import Image

from products.models import ProductPage, ProductIndexPage
from pages.models import HomePage, StoreFrontPage


class Command(BaseCommand):
    help = 'Create Baxter Award Pages'

    def handle(self, **options):
        data_src = os.path.join(settings.PROJECT_ROOT, 'data')

        StoreFrontPage.objects.all().delete()
        root_page = HomePage.objects.filter().get()

        categories = set()
        with open(os.path.join(data_src, 'grhistorysociety_store_items.csv')) as csvfile:
            products = csv.DictReader(csvfile)
            products = list(products)
            for row in products:
                categories.add(row['category'])

            storefront_index_page = StoreFrontPage(title='Storefront', intro='Please peruse at your leisure')
            root_page.add_child(instance=storefront_index_page)

            index_category_map = {category: ProductIndexPage(title=category) for category in categories}
            for index in index_category_map.values():
                storefront_index_page.add_child(instance=index)

            print('mapping', index_category_map)
            for row in products:
                c = row['category']
                print('got', type(index_category_map[c]))
                index_category_map[c].add_child(instance=ProductPage(
                    title=row['title'],
                    price=row['price'],
                    member_price='10000',  #TODO: calculate actual price based on member_discount percent
                    description=row['description']
                ))

            storefront_index_page.save_revision().publish()
