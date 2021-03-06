from django.db import models
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel
)
from wagtail.search import index

from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag

from modelcluster.fields import ParentalKey
from utils.models import LinkFields, RelatedLink
from .event_utils import export_event


EVENT_AUDIENCE_CHOICES = (
    ('public', "Public"),
    ('private', "Private"),
)


class EventIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('events.EventIndexPage', related_name='related_links')


class EventIndexPage(Page):
    subtitle = models.CharField(max_length=255, blank=True, help_text="This will override the title of the page.")
    intro = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    subpage_types = ['EventPage']

    @property
    def future_events(self):
        events = EventPage.objects.live()
        events = events.filter(date_from__gte=date.today())
        events = events.order_by('date_from')

        return events

    @property
    def past_events(self):
        events = EventPage.objects.live()
        events = events.filter(date_from__lte=date.today())
        events = events.order_by('-date_from')

        return events

    def get_context(self, request):
        # Get events
        events = self.future_events
        past = request.GET.get('past')

        if past:
            events = self.past_events
        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            events = events.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(events, 9)  # Show 10 events per page
        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        # Update template context
        context = super(EventIndexPage, self).get_context(request)
        context['events'] = events
        context['tags'] = Tag.objects.filter(
            events_eventpagetag_items__isnull=False,
            events_eventpagetag_items__content_object__live=True
        ).distinct().order_by('name')
        return context


EventIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="subtitle"),
    FieldPanel('intro', classname="full"),
    InlinePanel('related_links', label="Related links"),
]


EventIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]


class EventPageSpeaker(Orderable, LinkFields):
    page = ParentalKey('events.EventPage', related_name='speakers')
    full_name = models.CharField("Name", max_length=255, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    @property
    def name_display(self):
        return self.full_name

    panels = [
        FieldPanel('full_name'),
        ImageChooserPanel('image'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]


class EventPageTag(TaggedItemBase):
    content_object = ParentalKey('events.EventPage',
                                 related_name='tagged_items')


class EventPage(Page):
    subtitle = models.CharField(max_length=255, blank=True, help_text="This will override the title of the page.")
    date_from = models.DateField("Start date")
    date_to = models.DateField(
        "End date",
        null=True,
        blank=True,
        help_text="Not required if event is on a single day"
    )
    time_from = models.TimeField("Start time", null=True, blank=True)
    time_to = models.TimeField("End time", null=True, blank=True)
    audience = models.CharField(
        max_length=255, choices=EVENT_AUDIENCE_CHOICES, null=True, blank=True
    )
    location = models.CharField(max_length=255, null=True, blank=True)
    body = RichTextField(blank=True)
    cost = models.CharField(max_length=255, null=True, blank=True)
    signup_link = models.URLField(blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    tags = ClusterTaggableManager(through=EventPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('get_audience_display'),
        index.SearchField('location'),
        index.SearchField('body'),
    ]

    parent_page_types = ['events.EventIndexPage']

    @property
    def event_index(self):
        return self.get_ancestors().type(EventIndexPage).last()

    def serve(self, request):
        if "format" in request.GET:
            if request.GET['format'] == 'ical':
                # Export to ical format
                response = HttpResponse(
                    export_event(self, 'ical'),
                    content_type='text/calendar',
                )
                content_dispo = 'attachment; filename=' + self.slug + '.ics'

                response['Content-Disposition'] = content_dispo
                return response
            else:
                message = 'Could not export event\n\nUnrecognised format: ' + \
                    request.GET['format']
                return HttpResponse(message, content_type='text/plain')
        else:
            return super(EventPage, self).serve(request)


EventPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="subtitle"),
    FieldPanel('date_from'),
    FieldPanel('date_to'),
    FieldPanel('time_from'),
    FieldPanel('time_to'),
    FieldPanel('location'),
    FieldPanel('audience'),
    FieldPanel('cost'),
    FieldPanel('signup_link'),
    FieldPanel('tags'),
    FieldPanel('body', classname="full"),
    InlinePanel('speakers', label="Speakers"),
]

EventPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]
