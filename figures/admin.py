from django.contrib import admin

from . import models

# Register your models here.
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbr')
    search_fields = ('name', 'abbr')

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('no', 'state', 'dem_nom', 'rep_nom')
    search_fields = ('no', 'state', 'dem_nom', 'rep_nom')

admin.site.register(models.State, StateAdmin)
admin.site.register(models.District, DistrictAdmin)