# Generated by Django 3.1.13 on 2021-10-19 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SsOffice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, choices=[('FO', 'Field Office (FO)'), ('DDS', 'Disability Determination Services (DDS)'), ('OHO', 'Office of Hearings Operations (OHO)'), ('AC', 'Appeals Council (AC)'), ('PC', 'Program Service Center (PSC)'), ('RO', 'Regional Office (RO)'), ('NHC', 'National Hearing Center (NHC)'), ('CSU', 'Central Scheduling Unit (CSU)'), ('NCAC', 'National Case Assistance Center (NCAC'), ('WSU', 'Workload Support Unit (WSU)')], max_length=30, null=True)),
                ('slug', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('display_name', models.CharField(max_length=50, null=True)),
                ('ssa_site_code', models.CharField(max_length=128, null=True)),
                ('ssa_office_name', models.CharField(blank=True, max_length=128, null=True)),
                ('region', models.CharField(blank=True, max_length=20, null=True)),
                ('ssa_last_updated', models.CharField(max_length=50, blank=True, null=True)),
                ('address1', models.CharField(blank=True, max_length=128, null=True)),
                ('address2', models.CharField(blank=True, max_length=128, null=True)),
                ('city', models.CharField(blank=True, max_length=128, null=True)),
                ('state', models.CharField(blank=True, max_length=128, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=128, null=True)),
                ('tel_public', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('tel_call_back', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('tel_admin', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('efile_fax', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('servicing_states', models.CharField(blank=True, max_length=128, null=True)),
                ('servicing_fos', models.CharField(blank=True, max_length=128, null=True)),
                ('servicing_zipcodes', models.CharField(blank=True, max_length=128, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('notes', models.TextField(blank=True, max_length=128, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'SS Office',
                'verbose_name_plural': 'SSA Offices',
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='SsStaff',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('staff_type', models.CharField(blank=True, choices=[('ADM', 'Asst District Manager, FO'), ('ALJ', 'Administrative Law Judge, OHO'), ('CR', 'Claims Representative, FO'), ('DE', 'Disability Examiner, DDS'), ('DM', 'District Manager, FO'), ('GS', 'Group Supervisor, OHO'), ('HA', 'Hearing Asst, OHO'), ('HOD', 'Hearing Office Director'), ('OHO', 'Office of Hearings Operations'), ('OS', 'Operations Supervisor, FO'), ('PCS', 'Program Service Center Staff'), ('SA', 'Staff Attorney, OHO'), ('VDE', 'Vocational Disability Examiner, DDS'), ('CSU', 'CSU Staff')], max_length=20)),
                ('first_name', models.CharField(blank=True, max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('salutation', models.CharField(blank=True, max_length=128)),
                ('familiar_name', models.CharField(blank=True, max_length=128)),
                ('tel', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('tel_ext', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('notes', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('ss_office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ssoffices.ssoffice')),
                ('supervisor', models.ManyToManyField(blank=True, to='ssoffices.SsStaff')),
            ],
            options={
                'verbose_name': 'SSA Staff',
                'verbose_name_plural': 'SSA Staff',
                'ordering': ['last_name', 'first_name', 'ss_office'],
            },
        ),
    ]
