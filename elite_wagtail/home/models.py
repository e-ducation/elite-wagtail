import uuid
import re

from django.db import models
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
)
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel,
    HelpPanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.api import APIField
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock as OldImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.api.v2.serializers import ImageSerializer

from django_select2.forms import Select2MultipleWidget
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase, Tag as TaggitTag

from .routes import ArticleListRoutes

from rest_framework.fields import DateTimeField

COURSE_KEY_REGEX = r'courses/(?:[^/+]+(/|\+)[^/+]+(/|\+)[^/?]+)/'

NOTICE_HTML = """
【提示语句】<br/>
- GDPR要求的隐私声明<br/>
出于性能测试、数据分析和市场营销等目的，英荔使用cookies及其他跟踪技术。使用本网站即表示您接受此项操作。请在&lt;a href="http://www.baidu.com"&gt;“隐私政策”&lt;/a&gt;中了解更多相关技术的信息。<br/>

- 特殊事项公告<br/>
&lt;span style="color:#2e313c"&gt;版本更新通知：&lt;/span&gt;英荔商学院将迎来版本升级，于&lt;span style="color:#2e313c;"&gt;3月22日晚21:00至23:00&lt;/span&gt;进行服务器更新。届时部分功能的使用将受到影响，敬请期待更优质的新版体验~届时部分功能的使用将受到影响，敬请期待更优质的&lt;span style="color:#2e313c;"&gt;新版体验&lt;/span&gt;。<br/>

- 广告推送<br/>
营销的真正秘诀是什么？美国MBA教授给你不一样的答案。长岛大学商学院市场营销及国际商务系主任张东隆教授的新课程《营销管理与应用》上线啦！新学员限时优惠。
"""


class ImageChooserBlock(OldImageChooserBlock):
    def get_api_representation(self, value, context=None):
        """
        Override for output img url.
        """
        try:
            return value.file.url
        except Exception:
            return value


class CourseUrlBlock(blocks.URLBlock):
    def get_api_representation(self, value, context=None):
        """
        Override for output course url.
        """
        extract_course_url = re.search(COURSE_KEY_REGEX, value)
        if extract_course_url:
            return extract_course_url.group(0).replace('courses/', '').replace('/', '')
        else:
            return ''


@register_setting
class GoogleSettings(BaseSetting):
    analytics_account = models.CharField(max_length=127, blank=True,
                                         help_text='Your Google Analytics Account, UA-xxxxx')


@register_setting
class BaiduBridgeSettings(BaseSetting):
    url = models.URLField(
        help_text='Your Baidu Bridge URL')


@register_setting
class PopularArticleSettings(BaseSetting):
    display_popular_articles = models.BooleanField(
        default=True,
        verbose_name=_('Display popular articles')
    )


@register_setting
class ImportantPages(BaseSetting):
    bridge_page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL)

    panels = [
        PageChooserPanel('bridge_page'),
    ]


@register_setting
class EliteVariableSettings(BaseSetting):
    elite_filing_website = models.URLField(
        help_text='Your Elite Filing Website URL')
    elite_case_number = models.CharField(
        max_length = 32,
        help_text='Your Elite Case Number')


class BannerBlock(blocks.StructBlock):
    banners = blocks.ListBlock(blocks.StructBlock([
        ('image', ImageChooserBlock()),
        ('mobile_image', ImageChooserBlock()),
        ('link', blocks.URLBlock()),
    ]))
    loop_time = blocks.IntegerBlock(default=3000)

    class Meta:
        label = 'Banner'
        template = 'home/blocks/banner.html'
        icon = 'user'


class CourseBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock()
    description = blocks.CharBlock()
    link = CourseUrlBlock()
    publicity_page_url = blocks.URLBlock(required=False)

    class Meta:
        label = '推荐课程'
        template = 'home/blocks/course.html'
        icon = 'user'


class CategoriesListBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('模块标题'), default=_('课程分类'))
    categorieslist = blocks.ListBlock(blocks.StructBlock([
        ('categories_name', blocks.RegexBlock(regex=r'^[\u4e00-\u9fa5a-zA-Z]{2,10}$', error_messages={
            'invalid': _('只允许输入2到10位中英文字符')
        }, required=True, label=_('分类名称'))),
        ('categories_link', blocks.URLBlock(required=True, label=_('分类链接'))),
        ('img_for_app', ImageChooserBlock(required=False, label=_('app显示图标'))),
    ]), label=_('课程分类'))

    class Meta:
        template = 'home/blocks/categorieslist.html'
        label = "课程分类"
        icon = 'grip'


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
        label = "故事模块"
        icon = 'user'
        template = 'home/blocks/story.html'


class OtherImgBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('模块标题'))
    fill_the_screen_or_nor = blocks.BooleanBlock(label=_('是否撑满屏幕'), required=False)

    img_for_pc = ImageChooserBlock(required=True, label=_('PC端图片'))
    img_for_MOBILE = ImageChooserBlock(required=False, label=_('移动端图片'))

    link = blocks.URLBlock(required=False, label=_('链接(非必填)'))

    class Meta:
        label = "其余图文"
        icon = 'user'

        template = 'home/blocks/otherimg.html'


class ProfessorBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('模块标题'))
    professor_image = ImageChooserBlock(label=_('宣传图片'))

    professor = blocks.ListBlock(blocks.StructBlock([
        ('name', blocks.CharBlock(required=False, label=_('教授名称'))),
        ('professor_pic', ImageChooserBlock(required=False, label=_('教授头像'))),
        ('professor_link', blocks.URLBlock(required=False, label=_('链接'))),
        ('professor_degree', blocks.ListBlock(blocks.TextBlock(required=False), label=_('教授学历'))),
        ('content', blocks.CharBlock(required=False, label=_('内容'))),
    ]), label=_('教授'))

    professor_link = blocks.URLBlock(label=_('宣传链接'))

    class Meta:
        label = "教授模块"
        icon = 'user'
        template = 'home/blocks/professor.html'


class VipBlock(blocks.StructBlock):
    background_image = ImageChooserBlock(label=_('背景图片'))
    background_cotent = blocks.CharBlock(required=False, label=_('背景内容'))
    title = blocks.CharBlock(label=_('标题'))
    background_link = blocks.URLBlock(label=_('链接'))

    class Meta:
        label = "加入会员"
        icon = 'user'
        template = 'home/blocks/vip.html'


class SeriesProcessBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_('模块标题'))
    has_update_or_nor = blocks.BooleanBlock(label=_('是否有敬请期待'), required=False)
    series = blocks.ListBlock(blocks.StructBlock([
        ('course_photo', ImageChooserBlock(required=True, label=_('课程图片'))),
        ('title', blocks.CharBlock(required=True, label=_('课程标题'))),
        ('description', blocks.CharBlock(required=True, label=_('课程描述'))),
        ('link', blocks.URLBlock(required=True, label=_('课程链接'))),
    ]), label=_('课程路径'))

    class Meta:
        icon = 'user'
        label = "系列课程流程列表"
        template = 'home/blocks/series_process_list.html'


class SeriesBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock()
    description = blocks.CharBlock()
    link = blocks.URLBlock()

    class Meta:
        label = '系列课程'
        icon = 'user'


class HomePage(Page):
    advert = models.ForeignKey(
        'home.Advert',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField([
        ('Paragraph', blocks.RichTextBlock()),
        ('Image', ImageChooserBlock()),
        ('OtherImgBlock', OtherImgBlock()),
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

        ('Banner', BannerBlock()),
        ('Embed', EmbedBlock()),
        ('RecommendCourse', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('courses', blocks.ListBlock(CourseBlock()))
        ], template='home/blocks/recommend_courses.html')),
        ('SeriesCourse', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('series', blocks.ListBlock(SeriesBlock()))
        ], template='home/blocks/series_list.html')),
        ('StoryBlock', StoryBlock()),
        ('ProfessorBlock', ProfessorBlock()),
        ('CategoriesListBlock', CategoriesListBlock()),
        ('SubjectCourse', blocks.StructBlock([
            ('required_course', blocks.ListBlock(SeriesBlock())),
            ('optional_course', blocks.ListBlock(SeriesBlock()))
        ], template='home/blocks/subject_course.html')),
        ('VipBlock', VipBlock()),
        ('SeriesProcessBlock', SeriesProcessBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        SnippetChooserPanel('advert'),
    ]

    api_fields = [
        APIField('body'),
    ]


class ArticleListPage(ArticleListRoutes, Page):
    display_tags = models.BooleanField(default=True, verbose_name=_('Display tags'))
    num_entries_page = models.IntegerField(default=5, verbose_name=_('Entries per page'))
    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel('display_tags'),
            ],
            heading=_("Widgets")
        ),
        MultiFieldPanel(
            [
                FieldPanel('num_entries_page'),
            ],
            heading=_("Parameters")
        ),
    ]
    subpage_types = ['ArticlePage']

    def get_entries(self):
        return ArticlePage.objects.descendant_of(self).live().order_by('-article_datetime')

    def get_context(self, request, *args, **kwargs):
        context = super(ArticleListPage, self).get_context(request, *args, **kwargs)
        context['entries'] = self.entries
        context['article_page'] = self
        return context

    class Meta:
        verbose_name = _('ArticleList')


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey('home.ArticlePage', on_delete=models.CASCADE, related_name='tagged_items')


class ArticlePage(Page):
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    author_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    author_name = models.CharField(max_length=10, validators=[
        MinLengthValidator(2)
    ])
    article_datetime = models.DateTimeField()
    article_cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    article_cover_app = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    description = models.TextField(blank=True)
    liked_count = models.IntegerField(default=0)

    body = StreamField([
        ('Paragraph', blocks.RichTextBlock()),
        ('RawHTML', blocks.RawHTMLBlock()),
        ('DocumentChooser', DocumentChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        HelpPanel('建议文章标题不超过30个字'),
        FieldPanel('tags'),
        HelpPanel('建议标签数量最多2个，标签字数1～5个'),
        FieldPanel('description'),
        ImageChooserPanel('author_image'),
        FieldPanel('author_name'),
        FieldPanel('article_datetime'),
        ImageChooserPanel('article_cover'),
        ImageChooserPanel('article_cover_app'),
        StreamFieldPanel('body'),
    ]

    api_fields = [
        APIField('tags'),
        APIField('author_image'),
        APIField('author_name'),
        APIField('article_datetime', serializer=DateTimeField(format="%Y-%m-%d %H:%M")),
        APIField('article_cover'),
        APIField('article_cover_app'),
        APIField('description'),
        APIField('liked_count'),
        # This will nest the relevant BlogPageAuthor objects in the API response
    ]

    parent_page_types = ['ArticleListPage']
    subpage_types = []

    def get_datetime_format(self):

        return self.article_datetime.strftime("%Y-%m-%d %H:%I")

    @property
    def first_tag(self):
        if self.tags:
            return self.tags.first()
        else:
            return None


@register_snippet
class PopularArticle(Orderable):
    RANDOM_STRATEGY = (
        ('liked', 'liked'),
        ('last_published_at', 'last_published_at'),
    )

    title = models.CharField(max_length=5, validators=[
        MinLengthValidator(2),
    ])
    right_link = models.URLField(blank=True)
    use_random_article = models.BooleanField(default=False)
    random_num = models.IntegerField(default=3)
    random_strategy = models.CharField(
        choices=RANDOM_STRATEGY,
        max_length=32,
        default='liked'
    )
    selected_articles = models.ManyToManyField(ArticlePage, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('right_link'),
        FieldPanel('use_random_article'),
        FieldPanel('random_num'),
        FieldPanel('random_strategy'),
        FieldPanel('selected_articles', widget=Select2MultipleWidget),
        HelpPanel('建议选择3～8篇文章'),
    ]

    def __str__(self):
        return self.title

    def get_random_popular_articles(self):
        if self.random_strategy == 'liked':
            return ArticlePage.objects.all().order_by('liked_count')[:self.random_num]
        if self.random_strategy == 'last_published_at':
            return ArticlePage.objects.all().order_by('last_published_at')[:self.random_num]

        return None

    @property
    def articles(self):
        if self.use_random_article:
            return self.get_random_popular_articles()
        else:
            return self.selected_articles.all()


class NewHelpPanel(HelpPanel):

    def render(self):
        return render_to_string(self.template, {
            'self': self
        })


@register_snippet
class Advert(models.Model):
    ONCE = 1
    ONCE_A_DAY = 2
    PAGE_REQUEST_EACH_TIME = 3

    PUSH_CHOICES = (
        (ONCE, _("只弹一次")),
        (ONCE_A_DAY, _("每天弹出一次")),
        (PAGE_REQUEST_EACH_TIME, _("每次打开页面弹一次")),
    )

    ADV_TYPE_1 = 1
    ADV_TYPE_2 = 2
    ADV_TYPE_3 = 3

    ADV_TYPE_CHOICE = (
        (ADV_TYPE_1, _("GDPR要求的隐私声明")),
        (ADV_TYPE_2, _("特殊事项公告")),
        (ADV_TYPE_3, _("广告推送")),
    )

    title = models.CharField(verbose_name=_('广告标题'), max_length=5, validators=[
        MinLengthValidator(2),
    ])
    update_id = models.UUIDField(blank=True)
    raw_html = models.TextField(verbose_name=_('广告正文'))
    adv_status = models.IntegerField(choices=PUSH_CHOICES, default=ONCE, verbose_name=_('广告弹窗频率'))

    adv_type = models.IntegerField(choices=ADV_TYPE_CHOICE, default=ONCE, verbose_name=_('广告弹窗类型'))
    type3_url = models.URLField(blank=True, verbose_name=_('广告推送需要的链接'))

    panels = [
        FieldPanel('title'),
        FieldPanel('adv_status'),
        FieldPanel('raw_html'),
        FieldPanel('adv_type'),
        FieldPanel('type3_url'),
        HelpPanel(NOTICE_HTML),
    ]

    def save(self, *args, **kwargs):
        self.update_id = uuid.uuid1()
        super(Advert, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserFeedBack(models.Model):
    
    image_url = models.CharField(verbose_name=_('图片'), max_length=500)
    nick_name = models.CharField(blank=True,max_length=30, verbose_name=_('用户昵称'))
    content = models.TextField(verbose_name=_('反馈内容'))
    contact = models.CharField(blank=True,max_length=30, verbose_name=_('联系方式'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('提交时间'))
    
    panels = [
        FieldPanel('image_url'),
        FieldPanel('nick_name'),
        FieldPanel('content'),
        FieldPanel('contact'),
    ]
    class Meta(object):
    
        verbose_name = _("用户反馈")
        verbose_name_plural = _("用户反馈")

    def __str__(self):
        return self.nick_name       

