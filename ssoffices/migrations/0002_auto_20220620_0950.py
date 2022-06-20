# Generated by Django 3.2.8 on 2022-06-20 13:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ssoffices', '0001_initial'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='ssstaff',
        #     name='supervisor',
        #     field=models.ManyToManyField(blank=True, to='ssoffices.SsStaff'),
        # ),
        migrations.AlterField(
            model_name='ssoffice',
            name='type',
            field=models.CharField(blank=True, choices=[('FO', 'Field Office (FO)'), ('DDS', 'Disability Determination Services (DDS)'), ('HO', 'Office of Hearings Operations (OHO)'), ('AC', 'Appeals Council (AC)'), ('PC', 'Program Service Center (PSC)'), ('RO', 'Regional Office (RO)'), ('NHC', 'National Hearing Center (NHC)'), ('CSU', 'Central Scheduling Unit (CSU)'), ('NCAC', 'National Case Assistance Center (NCAC'), ('WSU', 'Workload Support Unit (WSU)')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='ssstaff',
            name='staff_type',
            field=models.CharField(blank=True, choices=[('ADM', 'Asst District Manager, FO'), ('ALJ', 'Administrative Law Judge, OHO'), ('CR', 'Claims Representative, FO'), ('DE', 'Disability Examiner, DDS'), ('DM', 'District Manager, FO'), ('GS', 'Group Supervisor, OHO'), ('HA', 'Hearing Asst, OHO'), ('HOD', 'Hearing Office Director'), ('HOS', 'Office of Hearings Operations (OHO) Staff'), ('OS', 'Operations Supervisor, FO'), ('PCS', 'Program Service Center Staff'), ('SA', 'Staff Attorney, OHO'), ('VDE', 'Vocational Disability Examiner, DDS'), ('CSU', 'CSU Staff')], max_length=20),
        ),
    ]
