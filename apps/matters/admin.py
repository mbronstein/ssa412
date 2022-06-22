from django.contrib import admin
from .models import Matter


class MatterAdmin(admin.ModelAdmin):
    search_fields = ('slug',)
    ordering = ["slug"]
    list_filter = ("slug", "type")


admin.site.register(Matter, MatterAdmin)
