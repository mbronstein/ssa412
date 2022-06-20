from django.db import models
from uuid import uuid4
import environ
from post_office import mail

env = environ.Env()

class OutgoingFax(models.Model):

    class FaxServiceStatus (models.TextChoices):
        DFT= ('DFT', "Draft")
        RTS = ('RTS', "Ready to Send")
        SENT = ('SENT', "Sent")
        SC = ('SC', 'Send Confirmed')


    id = models.BigAutoField(primary_key=True)
    recip_id = models.ForeignKey(on_delete=models.CASCADE, null=True, to="contacts")
    matter_id = models.ForeignKey(on_delete=models.CASCADE, null=True, to="matters", related_name='faxes')
    uuid = models.UUIDField(default=uuid4)
    sender_name = models.CharField(max_length=128)
    sender_faxnum = models.CharField(max_length=128)
    recip_name = models.CharField(max_length=128)
    recip_faxnum = models.CharField(max_length=128)
    add_coversheet = models.BooleanField(default=False)
    cs_subject = models.CharField(max_length=128, blank=True, default='')
    cs_body= models.TextField( blank=True, default='')
    file_to_fax = models.FileField
    has_coversheet = models.BooleanField(default=False)
    templatefile = models.CharField(max_length=128,null=True, blank=True)
    status = models.CharField(max_length=128, default='DRAFT', blank=True)
    sent_timestamp = models.DateTimeField(blank=True, null=True)
    receipt_confirmed = models.DateTimeField(blank=True, null=True)




    def send_by_email(self) :
        fax_service_account = env.str('FAX_SERVICE_ACCT')
        fax_service_password = env.str('FAX_SERVICE_PASSWORD')
        fax_server_email = env.str('FAX_SERVER_EMAIL')
        body=self.cs_body
        mail.send(recipients=fax_server_email,
                  subject=fax_service_account,
                  message=body
        )
        #todo add loggin
