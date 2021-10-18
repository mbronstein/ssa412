from django.core.management.base import BaseCommand
from ss411.ssoffices.models import SsOffice
import os
import csv
import phonenumbers


class Command(BaseCommand):
    help = 'our help string comes here'

    def _import_recs(self):
        fn = "ro-oho.csv"
        ScriptDir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(ScriptDir, fn)
        with open(filepath, "r") as data:
            for o in csv.DictReader(data):
                    newSSO = SsOffice()
                    #office_code as is
                    setattr(newSSO, "type", o.get("type", ""))
                    setattr(newSSO, "site_code", o.get("sitecode", ""))
                    # setattr(newSSO, "ssa_office_name", o.get("ssa_office_name", ""))
                    setattr(newSSO, "address1", o.get("address1", "").title())
                    setattr(newSSO, "address2", o.get("address2", "").title())
                    setattr(newSSO, "city", o.get("city", "").title())
                    setattr(newSSO, "state", o.get("state", ""))
                    setattr(newSSO, "zipcode", o.get("zipcode", ""))
                    try:
                        setattr(newSSO,
                                "tel_public",
                                phonenumbers.format_number(phonenumbers.parse(o.get("telephone",None),
                                                                              "US"),
                                                            phonenumbers.PhoneNumberFormat.E164
                                                            )
                                )
                    except:
                        setattr(newSSO, "tel_public","")
                    try:
                        setattr(newSSO,
                                "fax",
                                phonenumbers.format_number(phonenumbers.parse(o.get("fax", ""),
                                                                              "US"),
                                                            phonenumbers.PhoneNumberFormat.E164
                                                           )
                                )
                    except:
                        setattr(newSSO, "fax",None)
                    try:
                        setattr(newSSO,
                                "efile_fax",
                                phonenumbers.format_number(phonenumbers.parse(o.get("efile_fax", None),
                                                                              "US"),
                                                            phonenumbers.PhoneNumberFormat.E164
                                                            )
                                )
                    except:
                        setattr(newSSO, "efile_fax","")


                    #set slug to city-state-type
                    setattr(newSSO, "slug", f"{newSSO.city.lower().replace(' ', '-')}-{newSSO.state.lower()}-{newSSO.type.lower()}")
                    setattr(newSSO, "display_name", f"{newSSO.city.capitalize()} {newSSO.state.upper()} {newSSO.type.upper()}")
                    setattr(newSSO, 'ssa_last_updated', '2020-10-01')
                    setattr(newSSO, 'region', o.get("region", None))
                    setattr(newSSO, 'latitude', o.get("lat", None))
                    setattr(newSSO, 'longitude', o.get("lng", None))

                    try:

                        newSSO.save()

                    except Exception as e:
                        print("Error ", e.__class__, "occurred" )
                        print(newSSO.as_dict())

                        print()

    def handle(self, *args, **options):
        self._import_recs()
