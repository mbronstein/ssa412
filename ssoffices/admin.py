from django.contrib import admin
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from import_export.admin import ImportExportModelAdmin
from .models import SsOffice, SsStaff


class SsStaffInline(admin.TabularInline):
    model = SsStaff
    fields = ('last_name', 'first_name', 'type', 'ssoffice', 'city', 'tel', 'tel_ext')
    list_editable = ('ssoffice')

class SsOfficeAdmin(admin.ModelAdmin):
    inlines = [SsStaffInline,]
    list_display = ('slug', 'type', 'ssa_site_code', 'ssa_office_name', 'display_name',
                    'tel_public', 'fax', 'address1', 'address2', 'city', 'state', 'zipcode',
                    'region', 'ssa_last_updated')
    list_editable = ("tel_public", "fax")
    search_fields = ('slug', )
    ordering = ["slug"]
    list_filter = ('type', 'state', 'region')

    # formfield_overrides = {
    #     PhoneNumberField: {'widget': PhoneNumberPrefixWidget},
    # }




admin.site.register(SsOffice, SsOfficeAdmin)


class SsStaffAdmin(ImportExportModelAdmin):
    readonly_fields = ('created_by', 'last_modified_by')
    search_fields = ["display_name", "slug"]
    ordering = ["display_name", "ssoffice"]
    #todo add personal fax
    list_display = ('display_name', 'type', 'ssoffice','tel', 'tel_ext',
                    )
    list_editable = ('type', 'ssoffice', 'tel', 'tel_ext')
    # list_filter = ('ssoffice', 'type')

    #
    # formfield_overrides = {
    #     PhoneNumberField: {'widget': PhoneNumberInternationalFallbackWidget},
    # # }

    # list_editable = ("tel_public", "fax")



admin.site.register(SsStaff, SsStaffAdmin)
#
# class JurByLocationFormAdmin(admin.ModelAdmin):
#     readonly_fields = ('modified',)
#
# admin.site.register(JurByLocation, JurByLocationFormAdmin)
