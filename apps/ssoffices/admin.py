from django.contrib import admin
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from admin_auto_filters.filters import AutocompleteFilter
from import_export.admin import ImportExportModelAdmin
from .models import SsOffice, SsStaff


# class SsStaffInline(admin.TabularInline):
#     model = SsStaff
#     fields = ('last_name', 'first_name', 'salutation','type', 'ssoffice', 'tel', 'tel_ext')
#     list_editable = ('ssoffice', 'type')


class StateFilter(AutocompleteFilter):
    title = 'State'
    field_name = 'state'

class SsOfficeAdmin(admin.ModelAdmin):

    # inlines = [SsStaffInline,]
    list_display = ('slug', 'type', 'ssa_site_code', 'ssa_office_name', 'display_name',
                    'tel_public', 'fax', 'address1', 'address2', 'city', 'state', 'zipcode',
                    'region', 'ssa_last_updated')
    list_editable = ("tel_public", "fax")
    search_fields = ['state', 'type']
    ordering = ["slug"]
    listfilter = StateFilter

    # formfield_overrides = {
    #     PhoneNumberField: {'widget': PhoneNumberPrefixWidget},
    # }




admin.site.register(SsOffice, SsOfficeAdmin)


class SsStaffAdmin(ImportExportModelAdmin):
    readonly_fields = ('created_by', 'last_modified_by')
    search_fields = ["last_name", "slug"]
    ordering = ["last_name", 'first_name', "ss_office"]
    #todo add personal fax
    list_display = ('last_name', 'first_name', 'staff_type', 'salutation','ss_office','tel', 'tel_ext',
                    )
    list_editable = ('staff_type', 'ss_office', 'tel', 'tel_ext')
    # list_filter = ['ss_office']

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
