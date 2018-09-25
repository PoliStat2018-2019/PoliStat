from django.contrib import admin

from . import models

# Register your models here.
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbr')

admin.site.register(models.State, StateAdmin)