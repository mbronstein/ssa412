from lomb_be.utils.models import MbBaseModel
# from contacts.models import Contact
# from entries.models.entry_data import EmailData, CallData, DocData, NoteData, SmsData
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from phonenumber_field.modelfields import PhoneNumberField
from email.message import EmailMessage
from uuid import uuid4

# from codes.models import Code  to create later out of various codes below


class EntryType(models.IntegerChoices):
    UNKNOWN = (0, "Unknown")
    EMAIL = (1, "Email")
    CALL = (2, "Call")
    DOC = (3, "Document")
    NOTE = (4, "Note")
    MEET = (5, 'Meeting')
    SMS = (6, 'SMS')
    EVENT = (7, 'Event')


class IO(models.IntegerChoices):
    UNKNOWN = (0, "Unknown")
    IN = (1, "In")
    OUT = (2, "Out")
    NA = (3, "N/A")  # for meetings? filenotes?


class Status(models.IntegerChoices):
    UNKNOWN = (0, "Unknown")
    NEW = (1, "New")
    OPEN = (2, "Active")  # TODO: or should it be open?
    DRAFT = (3, "Draft")
    SENT = (4, "Sent")
    OTHER = (5, "Other")

    # TODO: other entry statuses?, seperate workflow status?


class WorkFlowStatus(models.IntegerChoices):
    pass


class IncomingMedium(models.IntegerChoices):
    UNKNOWN = (0, "Unknown")
    MAIL = (1, "Mail")
    EMAIL = (2, "Email")
    FAX = (3, "Fax")
    SMS = (4, "SMS")
    HAND = (5, "Hand")  # TODO clarify if drafted docuemtn what source?
    DICTATION = (6, 'Dictation')
    OTHER = (9, "Other")


class OriginatorType(models.IntegerChoices):
    UNKNOWN = (0, "Unknown")
    CLIENT = (1, "Client")
    SSFO = (2, "SS Field Office")
    SSDDS = (3, "SS DDS")
    SSOHO = (4, "SS Hearing Office")
    SSPSC = (5, "SS Service Center")
    SSAC = (6, "SS Appeals Council")
    SSFC = (7, "Federal Court")
    INSCO = (8, "Ins Co")
    OURFIRM = (9, "Our Firm")
    HEALTHCARE_PROVIDER = (10, "Healthcare Provider")
    EMPLOYER = (11, "Employer")
    OTHER = (12, "Other")


class ReviewChoices(models.IntegerChoices):
    pass
    # TODO: see note at ReviewType below


class CategoryChoices(models.IntegerChoices):
    pass


RecipientType = OriginatorType  # TODO: are they identical?


# how specific should this be??
class DocType(models.IntegerChoices):
    UNKNOWN = (0, "Unknown")
    SS_FORM = (1, "SS Form")
    INS_FORM = (2, "Ins Co Form")
    FIRM_FORM = (3, "Firm form")
    FORM = (4, "Form")
    LETTER = (5, "Letter")
    MED_REC = (6, 'Med Record')
    EMAIL = (7, 'Email')
    OTHER = (8, "Other")


class DocStatus(models.IntegerChoices):
    UNKNOWN = 0, "Unknown"
    NEW = 1, "New"
    READ = 2, "Read"
    DRAFT = 3, "Draft"
    FINAL = 4, "Final"
    SENT = 5, "Sent"


EmailStatus = DocStatus


class Entry(MbBaseModel):
    id = models.AutoField()
    UUID = models.UUIDField(default=uuid4,
                          editable=False, primary_key=True)
    type = models.IntegerField(choices=EntryType.choices, default=EntryType.UNKNOWN)
    matter = models.ForeignKey("Matter",
                               on_delete=models.SET_NULL,
                               null=True)
    subject = models.CharField(max_length=100, blank=True)  # aka subject in email object
    memo = models.TextField(blank=True)
    content_author_note = models.CharField(max_length=100, blank=True)

    # recipient?:  client, us, agency?  dr? other?
    # content_recipient = models.ForeignKey("Contact",  # what if more than one recipient
    #                                       on_delete=models.SET_NULL,
    #                                       null=True)
    # content_recipient_note = models.CharField(max_length=100, blank=True)
    # related_contacts = models.ManyToManyField(Contact)
    in_out = models.IntegerField(choices=IO.choices,
                                 default=IO.UNKNOWN)

    #event fields
    content_date = models.DateField(blank=True)
    start = models.DateTimeField(blank=True)
    end = models.DateTimeField(blank=True)
    location = models.CharField(max_length=60, blank=True)
    # geolocation = models
    # attendees = models.ForeignKey("Contacts")
    organizer = models.CharField(max_length=60, blank=True)


    # if incoming date of doc, email, call, sms
    # if outgoing, date on final draft that is being sent out.

    # email related
    # email_file = models.ForeignKey("Email", on_delete=models.DO_NOTHING
    # emil_ccs = ?
    # email attachments?

    # call related
    phonenumber = PhoneNumberField()
    cid_info = models.CharField(max_length=30, blank=True)
    voice_file = models.FileField()

    # doc related

    # note related



    # tags and categories
    # categories do we need? what would them by

    # tags = TaggableManager()

    incoming_medium = models.IntegerField(choices=IncomingMedium.choices,
                                          default=IncomingMedium.UNKNOWN)

    # workflow fields
    new = models.BooleanField(default=True)
    # TODO overall flag for unreviewed new entry? or just use status
    status = models.IntegerField(choices=Status.choices, default=Status.UNKNOWN)  # will vary depending on entry type
    status_note = models.CharField(max_length=80, blank=True)

    # use recall_date to set a date for file review??
    # next_audit_date = models.DateField(blank=True)

    # timekeeping fields
    is_billable = models.BooleanField(default=False)
    time_spent = models.DecimalField(default=0, decimal_places=2,  max_digits=6)
    #  def_billing_quickcode = ?
    # default billing text= models.CharField(max_length=80, )
    # was_billed = models.BooleanField(default=False)
    # date_billed = models.DateField(blank=True)
    # invoice number?
    # category = models.IntegerField(choices=CategoryChoices, default=0)
    # Todo should I have review codes or just set tasks and have a foreign key back to this record.
    # if so this would be done in the UI and would add entried to a related query which would show
    # up here as a back reference.
    # review_code = models.IntegerField(choices=ReviewChoices, default=0)
    # review_date = models.IntegerField(choices=ReviewChoices, default=0)
    #
    # last_review = models.DateField(max_length=30, blank=True)
    # review_interval = models.PositiveSmallIntegerField(default=30)

    date_received = models.DateField(blank=True)  # when received by LOMB

    # outgoing fields for docs/emails/sms being created by us.
    date_started = models.DateField(blank=True)  # started drafting
    date_sent = models.DateField(blank=True)  # date sent out
    recipient_type = models.IntegerField(choices=RecipientType.choices, default=RecipientType.UNKNOWN)
    recipient = models.CharField(max_length=80, default="unk")

    def __str__(self):
        return "??"

    class Meta:
        verbose_name_plural = "entries"
        app_label = "entries"


#
# class CallData(models.Model):
#
#     class Meta:
#         verbose_name_plural = "call_data_entries"
#
# class EmailData(IncomingEmail):
#     class Meta:
#         verbose_name_plural = "email_data_entries"
#
# class SmsData(models.Model):
#     class Meta:
#         verbose_name_plural = "sms_data_entries"
#
# class DocData(models.Model):
#     file = models.FileField()
#
#     class Meta:
#         verbose_name_plural = "doc_data_entries"
#
#
# class NoteData(models.Model):
#     class Meta:
#         verbose_name_plural = "note_entries"
#
    # class CategoryChoices(models.TextChoices):
    #     CASE_STATUS = "status", "Status"
    #     RESEARCH = "research", "Research"
    #     REVIEW = "review", "Review"
    #     EVENT_NOTES = "event-notes", "Event Notes"
    #     OTHER = "other", "Other"
    #     UNKNOWN = "unk", "Unknown"
    #
