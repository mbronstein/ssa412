# forms.py
from  django import forms
from .models import SsOffice, SsStaff

class SsOfficeList(forms.ModelForm):
    class Meta:
        model = SsOffice
        fields = fields = '__all__'

class SsStaffForm(forms.ModelForm):
    class Meta:
        model = SsStaff
        fields =  '__all__'

