from django.db import models

from django.conf import settings
from django.urls import reverse

from taggit.managers import TaggableManager


class Matter(models.Model):
    class Meta:
        app_label = "matters"
        ordering = ["slug"]
        verbose_name = "Matter"
        verbose_name_plural = "Matters"

    class MatterTypes(models.TextChoices):
        UNK = ('UNK', 'Unknown')
        SS = ('SS', 'Social Security/SSI')
        DI = ('DI', 'STD/LTD/ID')
        MH = ('MC', "Medicare")
        MC = ('MH', "MassHealth")
        EMP = ('EMP', "Employment")
        UIB = ('UIB', "Unemployoment Benefits")
        CR = ('CR', 'Credit/Loan')
        MIS = ('MIS', "Miscelenous")

    # class MatterSubTypes(models.Model):
    #     pass

    class StatusChoices(models.TextChoices):
        OP = ('OP', 'Open')
        CL = ('CL', 'Closed')
        RTC = ('RTC', 'Ready to Close')

    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=128,
                            choices=MatterTypes.choices,
                            null=True,
                            blank=True)
    # subtypes = models.Many?

    slug = models.CharField(max_length=128,
                            null=True,
                            blank=True,
                            unique=True)
    name = models.CharField(max_length=128,
                            null=True,
                            blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    # matter_contacts = models.ManyToManyField("MatterContact", null=True, related_name="contacts")
    date_opened = models.DateField(null=True)
    date_closed = models.DateField(null=True)
    status = models.CharField(max_length=128,
                              choices=StatusChoices.choices,
                              null=True,
                              blank=True)
    notes = models.TextField(max_length=128,
                             null=True,
                             blank=True)
    tags = TaggableManager()
    is_prospect = models.BooleanField(null=True, default=False)


    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='+',
                                    null=True,
                                    default=1
                                    )

    def __str__(self):
        return self.slug

    def __repr__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('matters:matters', kwargs={'slug': self.slug})

    def as_dict(self):
        return self.__dict__

# SUBTYPE_CHOICES = Choices(
#     (0, 'Unk', "Unknown"),
#     (1, 'initial', 'Initial Claim'),
#     (2, 'cdr', 'Continuing Dis Review (CDR)'),
#     (3, 'work', 'Work Issue'),
#     (4, 'op', 'Overpayment'),
#     (5, 'finance', 'SSI/Financial Issue'),
#     (6, 'misc', 'Miscellaneous'),
# )
