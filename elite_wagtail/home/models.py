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
    title = blocks.CharBlock(classname="course title")
    description = blocks.CharBlock(classname="course desc")

    class Meta:
        template = 'home/blocks/course.html'
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
            ('courses', blocks.ListBlock(
                CourseBlock(classname='course-item'),
                template='home/blocks/course_list.html'
            ))
        ], template='home/blocks/recommend_courses.html')),
    ])

    content_panels = [
        StreamFieldPanel('body'),
    ]
