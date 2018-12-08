import csv
import os
import decimal
from pathlib import Path

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from wagtail.images.models import Image

from products.models import ProductPage, ProductIndexPage
from pages.models import HomePage, StoreFrontPage

def get_decimal(dec, default=0.0):
    try:
        ret = decimal.Decimal(dec)
    except decimal.InvalidOperation:
        ret = default
    return ret

class Command(BaseCommand):
    help = 'Create Store Pages'

    def handle(self, **options):
        data_src = os.path.join(settings.PROJECT_ROOT, 'data')
        product_images_directory = os.path.join(settings.PROJECT_ROOT, 'data', 'store-images', 'cover')

        StoreFrontPage.objects.all().delete()
        root_page = HomePage.objects.filter().get()

        categories = set()
        with open(os.path.join(data_src, 'grhistorysociety_store_items.csv')) as csvfile:
            products = csv.DictReader(csvfile)
            products = list(products)
            for row in products:
                categories.add(row['category'])

            storefront_index_page = StoreFrontPage(title='Store', intro='Please peruse at your leisure',
                                                   show_in_menus=True)
            root_page.add_child(instance=storefront_index_page)

            index_category_map = {category: ProductIndexPage(title=category) for category in categories}
            for index in index_category_map.values():
                storefront_index_page.add_child(instance=index)

            for row in products:
                c = row['category']
                image_file_name = row['cover_image']
                image = self.get_product_image(product_images_directory, image_file_name)

                index_category_map[c].add_child(instance=ProductPage(
                    title=row['title'],
                    price=get_decimal(row['price']),
                    inventory=1,
                    shipping_cost=get_decimal(row['shipping_first_item']),
                    member_price='10000',  #TODO: calculate actual price based on member_discount percent
                    description=row['description'],
                    image=image
                ))

            storefront_index_page.save_revision().publish()

    def get_product_image(self, product_images_directory, image_name):
        try:
            with open( os.path.join(product_images_directory, image_name) , 'rb') as f:
                image_file = ImageFile(f, name='{}.jpg'.format(image_name))
                image = Image.objects.create(file=image_file)
                return image
        except (FileNotFoundError, IsADirectoryError):
            return None
