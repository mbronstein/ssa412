from django.contrib import admin
from .models import Entry

class EntryAdmin(admin.ModelAdmin):
    base_model = Entry

admin.register(Entry)

# class CallAdmin(EntryChildAdmin):
#     base_model = Entry  # Explicitly set here!
#     show_in_index = True
#     # define custom features here
#
#     def formfield_for_choice_field(self, db_field, request, **kwargs):
#         if db_field.name == "status":
#             kwargs['choices'] = CallEntry.StatusChoices.choices
#         elif db_field.name == "category":
#             kwargs['choices'] = CallEntry.CategoryChoices.choices
#         elif db_field.name == "subcategory":
#             kwargs['choices'] = CallEntry.SubcategoryChoices.choices
#         elif db_field.name == "io_direction":
#             kwargs['choices'] = CallEntry.IoDirectionChoices.choices
#         elif db_field.name == "io_source":
#             kwargs['choices'] = CallEntry.IoSourceChoices.choices
#
#         return super().formfield_for_choice_field(db_field, request, **kwargs)
#
# @admin.register(EmailEntry)
# class EmailAdmin(EntryChildAdmin):
#     base_model = EmailEntry  # Explicitly set here!
#     show_in_index = True  # makes child model admin visible in main admin site
#     # define custom features here
#
#
# @admin.register(NoteEntry)
# class NoteAdmin(EntryChildAdmin):
#     base_model = NoteEntry  # Explicitly set here!
#     show_in_index = True  # makes child model admin visible in main admin site
#     # define custom features here
#
#
#
# @admin.register(EventEntry)
# class EventAdmin(EntryChildAdmin):
#     base_model = EventEntry  # Explicitly set here!
#     show_in_index = True  # makes child model admin visible in main admin site
#     # define custom features here
#
# @admin.register(DocEntry)
# class DocAdmin(EntryChildAdmin):
#     base_model = DocEntry  # Explicitly set here!
#     show_in_index = True  # makes child model admin visible in main admin site
#     # define custom features here
#
# @admin.register(TaskEntry)
# class TaskAdmin(EntryChildAdmin):
#     base_model = TaskEntry  # Explicitly set here!
#     show_in_index = True  # makes child model admin visible in main admin site
#     # define custom features here
#
# @admin.register(SmsEntry)
# class SmsAdmin(EntryChildAdmin):
#     base_model = SmsEntry  # Explicitly set here!
#     show_in_index = True  # makes child model admin visible in main admin site
#     # define custom features here
#
#
# @admin.register(Entry)
# class EntryParentAdmin(PolymorphicParentModelAdmin):
#     """ The parent model admin """
#     base_model = Entry
#     child_models = (CallEntry, EmailEntry, DocEntry, TaskEntry, NoteEntry, EventEntry, SmsEntry)
#     list_filter = (PolymorphicChildModelFilter,)  # This is optional.
