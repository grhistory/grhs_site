from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image

from decimal import Decimal


from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel
)
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from utils.models import RelatedLink
from wagtail.contrib.settings.models import BaseSetting, register_setting

# Product page
class ProductIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey(
        'products.ProductIndexPage', related_name='related_links'
    )


class ProductIndexPage(Page):
    subtitle = models.CharField(max_length=255, blank=True, help_text="This will override the title of the page.")
    intro = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    indexed_fields = ('intro', )

    subpage_types = ['ProductPage']

    @property
    def categories(self):
        return ProductIndexPage.objects.all()

    @property
    def products(self):
        return ProductPage.objects.live().descendant_of(self)

    @property
    def tag_list(self):
        tag_ids = ProductPageTag.objects.all().values_list('tag_id', flat=True)
        return Tag.objects.filter(pk__in=tag_ids)

    def get_context(self, request):
        # Get products
        products = self.products
        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            products = products.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(products, 12)  # Show 10 products per page
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        # Update template context
        context = super(ProductIndexPage, self).get_context(request)
        context['products'] = products
        context['categories'] = self.categories
        return context

ProductIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle'),
    FieldPanel('intro', classname="full"),
    InlinePanel('related_links', label="Related links"),
]


ProductIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]


class ProductPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('products.ProductPage', related_name='related_links')


class ProductPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'products.ProductPage', related_name='tagged_items'
    )

    def __unicode__(self):
        return self.name


class ProductPage(Page):
    subtitle = models.CharField(max_length=255, blank=True, help_text="This will override the title of the page.")
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=8)
    shipping_cost = models.DecimalField(default=0.0, decimal_places=2, max_digits=6, help_text="Shipping cost")
    inventory = models.IntegerField(default=1, help_text="Current inventory on hand. Items with 0 or blank will not be available for purchase.")
    member_price = models.DecimalField(default=0.0,decimal_places=2, max_digits=8)
    description = RichTextField(blank=True)
    intro = models.CharField(max_length=255, blank=True)
    link_demo = models.URLField("Demo link", blank=True)
    tags = ClusterTaggableManager(through=ProductPageTag, blank=True)
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feed_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    indexed_fields = ('title', 'intro', 'biography')

    def get_context(self, request):
        context = super(ProductPage, self).get_context(request)
        if request.user.is_authenticated:
            context['price'] = self.member_price
            context['cost'] = self.member_price + self.shipping_cost
        else:
            context['price'] = self.price
            context['cost'] = self.price + self.shipping_cost
        context['category'] = self.get_parent()
        return context

ProductPage.content_panels = [
    FieldPanel('title', classname="title"),
    FieldPanel('subtitle', classname="subtitle"),
    FieldPanel('intro', classname="full"),
    FieldPanel('price', classname="full"),
    FieldPanel('shipping_cost', classname="full"),
    FieldPanel('inventory', classname="full"),
    FieldPanel('member_price', classname="full"),
    FieldPanel('description', classname="full"),
    ImageChooserPanel('image'),
    FieldPanel('link_demo'),
    FieldPanel('tags'),
    InlinePanel('related_links', label="Related links"),
]

ProductPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]

@register_setting
class PaypalSettings(BaseSetting):
    identity_token = models.CharField(
        max_length=255,
        help_text='Enter your Paypal payment data transfer identity token'
    )
    url = models.CharField(
        max_length=255,
        help_text='Enter the Paypal URL',
        default='www.sandbox.paypal.com'
    )
    email = models.CharField(
            max_length=255,
            help_text='Enter your Paypal email address',
            default=''
    )

