from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.db import models
from django.contrib.admin import StackedInline
from django.contrib.auth.models import User, Permission

from django_summernote.admin import SummernoteModelAdmin
from django_summernote.admin import SummernoteInlineModelAdmin
from textwrap import dedent 

from . import models as my_models
from . import forms

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')

class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbr')
    search_fields = ('name', 'abbr')

class DistrictInlineProfile(StackedInline, SummernoteInlineModelAdmin):
    model = my_models.DistrictProfile
    max_num = 1
    min_num = 1
    fk_name = 'district'
    can_delete = False


class DistrictAdmin(admin.ModelAdmin):
    exclude = ('id',)
    readonly_fields = ('id',)
    list_display = ('no', 'state', 'dem_nom', 'rep_nom')
    search_fields = ('no', 'state__name', 'dem_nom', 'rep_nom')

    # def edit_profile_link(self, district):
    #     link = reverse('admin:figures_districtprofile_change',
    #                 args=[district.districtprofile.pk])

    #     return format_html(
    #         f'<a href="{link}">Edit {district.districtprofile}</a>'
    #     )
    # edit_profile_link.short_description = 'Edit district profile'

    inlines = (DistrictInlineProfile,)


class DistrictPostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)

    list_display = ('title', 'author', 'date')
    search_fields = ('title',
                     'author__username',
                     'author__email',
                     'author__first_name',
                     'author__last_name',
                     'date')


class BlogPostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)

    list_display = ('title', 'author', 'date')
    search_fields = ('title', 'author', 'date')


class AboutContentAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)
    list_display = ('date',)


# admin.site.register(my_models.User, UserAdmin)
admin.site.register(Permission)

admin.site.register(my_models.State, StateAdmin)
admin.site.register(my_models.District, DistrictAdmin)
admin.site.register(my_models.DistrictPost, DistrictPostAdmin)
admin.site.register(my_models.BlogPost, BlogPostAdmin)
admin.site.register(my_models.AboutContent, AboutContentAdmin)
