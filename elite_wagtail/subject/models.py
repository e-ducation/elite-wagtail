from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import (
    StreamFieldPanel,
)
from wagtail.images.blocks import ImageChooserBlock


# Create your models here.
class SubjectBlock(blocks.StructBlock):
    course_photo = ImageChooserBlock()
    title = blocks.CharBlock()
    description = blocks.CharBlock()
    link = blocks.URLBlock()

    class Meta:
        icon = 'user'


class SubjectPage(Page):
    body = StreamField([
        ('SubjectCourse', blocks.StructBlock([
            ('required_course', blocks.ListBlock(SubjectBlock())),
            ('optional_course', blocks.ListBlock(SubjectBlock()))
        ], template='subject/blocks/subject_course.html')),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
