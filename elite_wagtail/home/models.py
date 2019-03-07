from django.db import models
from django.utils.translation import ugettext_lazy as _

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

    title = blocks.CharBlock(label=_('模块标题'))
    propaganda_image = ImageChooserBlock(label=_('宣传图片'))

    story = blocks.ListBlock(blocks.StructBlock([
        ('story_photo', blocks.ListBlock(ImageChooserBlock(required=False), label=_('故事图片'))),
        ('story_title', blocks.CharBlock(required=False, label=_('故事标题'))),
        ('story_content', blocks.CharBlock(required=False, label=_('故事内容'))),
        ('photo_location', blocks.ChoiceBlock(choices=[
            ('left', 'left'),
            ('center', 'center'),
        ], icon='cup', label=_('图片位置'))),
        ('story_link', blocks.URLBlock(label=_('故事链接'))),
    ]), label=_('用户故事'))

    propaganda_link = blocks.URLBlock(label=_('宣传链接'))
 
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
