# tables.py
from .models import SsOffice
import django_tables2 as tables

class SsOfficeTable(tables.Table):
    class Meta:
        model = SsOffice
        fields = ("slug", "phone_public", "fax",)






