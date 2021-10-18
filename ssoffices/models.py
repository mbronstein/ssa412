from django.db import models

#list of all ssa office downloaded from
# https://www.ssa.gov/open/data/FO-RS-Address-Open-Close-Time-App-Devs.html#dataDictionary
# on 11/29/20

import uuid
from django.conf import settings
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


ROJurArray = None
OHOJurArray = None
DDSJurArray = None
PSCJurArray = None


def create_slug(city, state, type):
    return f"{city}-{state}-{type}".lower()


class SsOffice(models.Model):
    class Meta:
        app_label = "ssoffices"
        ordering = ["slug"]
        verbose_name = "SS Office"
        verbose_name_plural = "SSA Offices"

    class SsOfficeTypes(models.TextChoices):
        FO = ('FO', "Field Office (FO)")
        DDS = ('DDS', "Disability Determination Services (DDS)")
        OHO = ('OHO', "Office of Hearings Operations (OHO)")
        AC = ('AC', "Appeals Council (AC)")
        PC = ('PC', "Program Service Center (PSC)")
        RO =('RO', "Regional Office (RO)")
        NHC = ('NHC', "National Hearing Center (NHC)")
        CSU = ('CSU', "Central Scheduling Unit (CSU)")
        NCAC = ('NCAC', "National Case Assistance Center (NCAC")
        WSU = ('WSU', "Workload Support Unit (WSU)")

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    type = models.CharField(max_length=30, choices=SsOfficeTypes.choices, null=True, blank=True)
    slug = models.CharField(max_length=50, null=True, blank=True, unique=True)
    display_name = models.CharField(max_length=50, null=True)
    site_code = models.CharField(max_length=128, null=True)
    ssa_office_name = models.CharField(max_length=128, null=True, blank=True)
    region = models.CharField(max_length=20, null=True, blank=True)

    ssa_last_updated = models.DateField(null=True)
    # lookup_name = models.CharField(max_length=128)
    address1 = models.CharField(max_length=128, null=True, blank=True)
    address2 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    zipcode = models.CharField(max_length=128, null=True, blank=True)
    tel_public = PhoneNumberField(blank=True, null=True)
    tel_call_back = PhoneNumberField(blank=True, null=True)
    tel_admin = PhoneNumberField(blank=True, null=True)
    fax = PhoneNumberField(blank=True, null=True)
    efile_fax = PhoneNumberField(blank=True, null=True)
    servicing_states = models.CharField(max_length=128, null=True, blank=True)
    servicing_fos = models.CharField(max_length=128, null=True, blank=True)
    servicing_zipcodes = models.CharField(max_length=128, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    notes = models.TextField(max_length=128, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    # last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                                      on_delete=models.CASCADE,
    #                                      related_name='+',
    #                                      null=True,
    #                                      default=1
    #                                      )

    def __str__(self):
        return self.slug

    def __repr__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('ssoffices:ssoffices', kwargs={'slug': self.slug})

    def as_dict(self):
        return self.__dict__

    @property
    def city_state_zip(self):
        return f"{self.city}, {self.state}  {self.zipcode}"


class SsStaff(models.Model):
    class Meta:
        app_label = "ssoffices"
        verbose_name = "SSA Staff"
        verbose_name_plural = "SSA Staff"
        ordering = ['last_name', 'first_name', 'ss_office']

    class StaffTypes(models.TextChoices):
        ADM= ('ADM', "Asst District Manager, FO")
        ALJ = ('ALJ', "Administrative Law Judge, OHO")
        CR = ('CR', "Claims Representative, FO")
        DE = ('DE', "Disability Examiner, DDS")
        DM = ('DM', "District Manager, FO")
        GS = ('GS', "Group Supervisor, OHO")
        HA = ('HA', "Hearing Asst, OHO")
        HOD = ('HOD', "Hearing Office Director")
        OHO = ('OHO', "Office of Hearings Operations")
        OS = ('OS', "Operations Supervisor, FO")
        PCS = ('PCS', "Program Service Center Staff")
        SA = ('SA', "Staff Attorney, OHO")
        VDE =('VDE', "Vocational Disability Examiner, DDS")
        CSU = ('CSU', "CSU Staff")


    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True)
    ss_office = models.ForeignKey(SsOffice,
                                  on_delete=models.CASCADE)
    staff_type = models.CharField(choices=StaffTypes.choices,
                                  max_length = 20,
                                  blank = True)
    first_name = models.CharField(max_length=128,
                                  blank=True)
    last_name = models.CharField(max_length=128)
    salutation = models.CharField(max_length=128,
                                  blank=True)
    familiar_name = models.CharField(max_length=128,
                                     blank=True)
    tel = PhoneNumberField(blank=True)
    tel_ext = models.CharField(max_length=20,
                               blank=True)
    email = models.EmailField(blank=True)
    supervisor = models.ManyToManyField("SsStaff", blank=True)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name='+',
                                   null=True,
                                   )
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                         on_delete=models.CASCADE,
                                         related_name='+',
                                         null=True,
                                         )

    def __str__(self):
        return f"{self.last_name}, {self.first_name}, {self.staff_type},{self.ss_office}"

    def __repr__(self):
        return f"{self.last_name}, {self.first_name}, {self.staff_type}, {self.ss_office}"

    def display_name(self):
        return f"{self.last_name}, {self.first_name}, {self.staff_type}"
