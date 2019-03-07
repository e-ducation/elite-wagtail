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
    course_photo = ImageChooserBlock()
    title = blocks.CharBlock()
    description = blocks.CharBlock()
    link = blocks.URLBlock()

    class Meta:
        template = 'home/blocks/course.html'
        icon = 'user'

class StoryBlock(blocks.StructBlock):

    title = blocks.CharBlock()
    propaganda_image = ImageChooserBlock()

    story = blocks.ListBlock(blocks.StructBlock([
        ('story_photo', blocks.ListBlock(ImageChooserBlock(required=False))),
        ('story_title', blocks.CharBlock(required=False)),
        ('story_content', blocks.CharBlock(required=False)),
        ('photo_location', blocks.ChoiceBlock(choices=[
            ('left', 'left'),
            ('center', 'center'),
        ], icon='cup')),
        ('story_link', blocks.URLBlock()),
    ]))

    propaganda_link = blocks.URLBlock()
 
    class Meta:
        icon = 'user'
        template = 'home/blocks/story.html'


class SeriesBlock(blocks.StructBlock):
    course_photo = ImageChooserBlock()
    title = blocks.CharBlock()
    description = blocks.CharBlock()
    link = blocks.URLBlock()

    class Meta:
        icon = 'user'


class HomePage(Page):

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('text', blocks.TextBlock()),
        ('EmailBlock', blocks.EmailBlock()),
        ('IntegerBlock', blocks.IntegerBlock()),
        ('FloatBlock', blocks.FloatBlock()),
        ('DecimalBlock', blocks.DecimalBlock()),
        ('URLBlock', blocks.URLBlock()),
        ('BooleanBlock', blocks.BooleanBlock()),
        ('DateBlock', blocks.DateBlock()),
        ('TimeBlock', blocks.TimeBlock()),
        ('DateTimeBlock', blocks.DateTimeBlock()),
        ('RawHTMLBlock', blocks.RawHTMLBlock()),
        ('BlockQuoteBlock', blocks.BlockQuoteBlock()),

        ('ChoiceBlock', blocks.ChoiceBlock()),
        ('PageChooserBlock', blocks.PageChooserBlock()),
        ('DocumentChooserBlock', DocumentChooserBlock()),

        ('EmbedBlock', EmbedBlock()),
        ('RecommendCourse', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('courses', blocks.ListBlock(CourseBlock()))
        ], template='home/blocks/recommend_courses.html')),
        ('SeriesCourse', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('series', blocks.ListBlock(SeriesBlock()))
        ], template='home/blocks/series_list.html')),
        ('StoryBlock',StoryBlock()), 
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
