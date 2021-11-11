from django.contrib import admin
from .models import MergeForm


class MergeFormAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'last_modified_by')
    search_fields = ('name',)



admin.site.register(MergeForm, MergeFormAdmin)
