from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.db import models
from django.contrib.admin import StackedInline

from django_summernote.admin import SummernoteModelAdmin
from textwrap import dedent 

from . import models as my_models
from . import forms

# Register your models here.
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbr')
    search_fields = ('name', 'abbr')

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('no', 'state', 'dem_nom', 'rep_nom', 'edit_profile_link')
    search_fields = ('no', 'state__name', 'dem_nom', 'rep_nom')

    def edit_profile_link(self, district):
        link = reverse('admin:figures_districtprofile_change',
                    args=[district.districtprofile.pk])

        return format_html(
            f'<a href="{link}">Edit {district.districtprofile}</a>'
        )
    edit_profile_link.short_description = 'Edit district profile'


class DistrictProfileAdmin(SummernoteModelAdmin):
    summernote_fields = ('profile',)

    list_display = ('district', 'modified')
    search_fields = ('district__state__name', 'district__state__abbr', 'district__no', 'profile')


class BlogPostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)

    list_display = ('title', 'author', 'date_posted')
    search_fields = ('title', 'author', 'date_posted')

admin.site.register(my_models.State, StateAdmin)
admin.site.register(my_models.District, DistrictAdmin)
admin.site.register(my_models.DistrictProfile, DistrictProfileAdmin)
admin.site.register(my_models.BlogPost, BlogPostAdmin)