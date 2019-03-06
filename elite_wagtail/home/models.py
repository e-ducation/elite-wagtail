from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import (
    StreamFieldPanel,
)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock


class CourseBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock()
    description = blocks.CharBlock()
    link = blocks.URLBlock()

    class Meta:
        template = 'home/blocks/course.html'
        icon = 'user'


class SeriesBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock()
    description = blocks.CharBlock()
    link = blocks.URLBlock()

    class Meta:
        icon = 'user'


class HomePage(Page):

    body = StreamField([
        ('Paragraph', blocks.RichTextBlock()),
        ('Image', ImageChooserBlock()),
        ('Text', blocks.TextBlock()),
        ('Heading', blocks.CharBlock()),
        ('BlockQuote', blocks.BlockQuoteBlock()),
        ('Email', blocks.EmailBlock()),
        ('URL', blocks.URLBlock()),
        ('Boolean', blocks.BooleanBlock()),
        ('Integer', blocks.IntegerBlock()),
        ('Float', blocks.FloatBlock()),
        ('Decimal', blocks.DecimalBlock()),
        ('Date', blocks.DateBlock()),
        ('Time', blocks.TimeBlock()),
        ('DateTime', blocks.DateTimeBlock()),
        ('RawHTML', blocks.RawHTMLBlock()),

        ('Choice', blocks.ChoiceBlock()),
        ('PageChooser', blocks.PageChooserBlock()),
        ('DocumentChooser', DocumentChooserBlock()),

        ('Embed', EmbedBlock()),
        ('RecommendCourse', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('courses', blocks.ListBlock(CourseBlock()))
        ], template='home/blocks/recommend_courses.html')),
        ('SeriesCourse', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('series', blocks.ListBlock(SeriesBlock()))
        ], template='home/blocks/series_list.html')),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
