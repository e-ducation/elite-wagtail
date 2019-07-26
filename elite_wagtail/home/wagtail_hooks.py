from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)
from taggit.models import Tag
from home.models import ArticlePage, ArticlePageTag, UserFeedBack
from django.utils.translation import ugettext as _


class TagAdmin(ModelAdmin):
    model = Tag
    menu_label = 'Tag'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required
    menu_order = 201  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', )
    list_filter = ('name',)
    search_fields = ('name', )

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(TagAdmin)


class UserFeebackAdmin(ModelAdmin):
    model = UserFeedBack
    menu_label = _('用户反馈')  # ditch this to use verbose_name_plural from model
    # menu_icon = 'pilcrow'  # change as required
    menu_order = 99999 # will put in 3rd place (000 being 1st, 100 2nd)
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_per_page = 5
    list_display = ('id', 'nick_name', 'image_url', 'contact', 'content', 'create_date',)
    ordering = ('id',)
    # list_filter = ('id', 'nick_name', 'image_url', 'contact', 'content', 'create_date')
    search_fields = ('nick_name', 'contact', 'content')
    index_template_name = "home/userfeeback.html"
    
# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(UserFeebackAdmin)
