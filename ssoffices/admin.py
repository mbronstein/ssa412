from django.contrib import admin
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from import_export.admin import ImportExportModelAdmin
from .models import SsOffice, SsStaff


class SsStaffInline(admin.TabularInline):
    model = SsStaff
    fields = ('last_name', 'first_name', 'tel', 'tel_ext')
    # formfield_overrides = {
    #     PhoneNumberField: {'widget': PhoneNumberPrefixWidget},
    # }
class SsOfficeFormAdmin(admin.ModelAdmin):
    inlines = [SsStaffInline,]
    list_display = ('slug', 'type', 'ssa_site_code', 'ssa_office_name', 'display_name',
                    'tel_public', 'fax', 'address1', 'address2', 'city', 'state', 'zipcode',
                    'region', 'ssa_last_updated')

    search_fields = ('slug', 'type')
    ordering = ["slug"]

    # formfield_overrides = {
    #     PhoneNumberField: {'widget': PhoneNumberPrefixWidget},
    # }
    list_filter = ('type', 'state', 'region')
    list_editable = ("tel_public", "fax")



admin.site.register(SsOffice, SsOfficeFormAdmin)


class SsStaffFormAdmin(ImportExportModelAdmin):
    readonly_fields = ('created_by', 'last_modified_by')
    search_fields = ["last_name", "ss_office"]
    ordering = ["last_name", "first_name", "ss_office"]

    list_display = ('display_name', 'ss_office', 'tel', 'tel_ext', 'staff_type',
                    'email', 'notes',
                    )
    list_filter = ('last_name', 'ss_office')

    #
    # formfield_overrides = {
    #     PhoneNumberField: {'widget': PhoneNumberInternationalFallbackWidget},
    # # }

    # list_editable = ("tel_public", "fax")



admin.site.register(SsStaff, SsStaffFormAdmin)
#
# class JurByLocationFormAdmin(admin.ModelAdmin):
#     readonly_fields = ('modified',)
#
# admin.site.register(JurByLocation, JurByLocationFormAdmin)
