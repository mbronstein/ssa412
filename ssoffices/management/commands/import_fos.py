from django.core.management.base import BaseCommand
from ss411.ssoffices.models import SsOffice
import os
import csv


class Command(BaseCommand):
    help = 'our help string comes here'

    def _import_recs(self):
        fn = "foimportastext.csv"
        ScriptDir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(ScriptDir, fn)
        with open(filepath, "r") as data:



            for o in csv.DictReader(data):
                try:
                    newSSO = SsOffice()
                    #office_code as is
                    setattr(newSSO, "type", "FO")
                    setattr(newSSO, "ssa_office_code", o.get("ssa_office_code", ""))
                    setattr(newSSO, "ssa_office_name", o.get("ssa_office_name", ""))
                    setattr(newSSO, "address1", o.get("address1", "").title())
                    setattr(newSSO, "address2", o.get("address2", "").title())
                    setattr(newSSO, "city", o.get("city", "").title())
                    setattr(newSSO, "state", o.get("state", ""))
                    setattr(newSSO, "zipcode", o.get("zipcode", ""))
                    pn = o.get("tel_public", "")
                    new_pn = pn.replace("(",'+1').replace(") ","").replace('-',"")
                    setattr(newSSO, "tel_public", new_pn)
                    #set slug to the SSA's official name for the office plus '-fo'
                    setattr(newSSO, "slug", newSSO.ssa_office_name.lower().replace(" ", "-")+"-fo")
                    setattr(newSSO, "display_name", newSSO.ssa_office_name.capitalize()+' FO')
                    setattr(newSSO, 'ssa_last_updated', '2020-10-01')
                    newSSO.save()
                except Exception as e:
                    print("Oops!", e.__class__, "occurred.")
                    print(newSSO)
                    print("Next entry.")
                    print()

    def handle(self, *args, **options):
        self._import_recs()
