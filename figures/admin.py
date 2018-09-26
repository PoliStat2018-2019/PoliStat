from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from textwrap import dedent 

from . import models

# Register your models here.
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbr')
    search_fields = ('name', 'abbr')

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('no', 'state', 'dem_nom', 'rep_nom', 'edit_profile_link')
    search_fields = ('no', 'state__name', 'dem_nom', 'rep_nom')

    def edit_profile_link(self, district):
        if not hasattr(district, 'districtprofile'):
            dp = models.DistrictProfile.manager.create(
                district = district,
                profile = dedent("""
                    This text is automatically generated for each district.
                    Please change it; we do not want it on our site.
               """)
            )
            link = reverse('admin:figures_districtprofile_change',
                            args=[dp.pk])

            return format_html(
                f'<a href="{link}">Edit {dp}</a>'
            )
        else:
            link = reverse('admin:figures_districtprofile_change',
                        args=[district.districtprofile.pk])

            return format_html(
                f'<a href="{link}">Edit {district.districtprofile}</a>'
            )
    edit_profile_link.short_description = 'Edit district profile'


class DistrictProfileAdmin(admin.ModelAdmin):
    list_display = ('district', 'modified')
    search_fields = ('district__state__name', 'district__state__abbr', 'district__no', 'profile')


admin.site.register(models.State, StateAdmin)
admin.site.register(models.District, DistrictAdmin)
admin.site.register(models.DistrictProfile, DistrictProfileAdmin)