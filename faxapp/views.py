from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views.generic import TemplateView
from post_office import mail

# class EmailView(TemplateView):
#     did = '6173008926'
#     sender = 'Mark Bronstein'
#     sender_fax = '617-300-8926'
#     sender_email = 'mbronstein@bronsteinlaw.com'
#     fax_memo = ''
#
#     mail.send(
#         'recipient@example.com',
#         sender_email,
#         subject=did,
#         message=fax_memo
#         context = {'foo': 'bar'},
#         priority = 'now',
#         attachments = {
#             'attachment1.doc': '/path/to/file/file1.doc',
#             'attachment2.txt': ContentFile('file content'),
#             'attachment3.txt': {'file': ContentFile('file content'), 'mimetype': 'text/plain'},
#         }
#     )
