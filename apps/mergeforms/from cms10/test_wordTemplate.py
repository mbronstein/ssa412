from unittest import TestCase, skip
import os
from docxtpl import DocxTemplate




class TestDocxTemplate(TestCase):
    def setUp(self):
        self.APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
        self.FIXTURE_DIR = os.path.join(os.path.dirname(self.APP_DIR), 'fixtures')
        self.FORM_DIR = os.path.join(self.APP_DIR, 'static', 'formlib')

    def test_render1(self):
        doc = DocxTemplate(os.path.join( self.FIXTURE_DIR, 'test_docx.docx'))
        context = {'claimant_full_name':"Mary Smith", 'claimant_ssn': '111-22-1234'}
        doc.render(context)
        doc.save(os.path.join(self.FIXTURE_DIR, 'generated_doc.docx'))

    def test_render2(self):
        doc = DocxTemplate(os.path.join( self.FIXTURE_DIR,'do-letter-form.docx'))
        context = {'claimant_full_name':"Mary Smith", 'claimant_ssn': '111-22-1234'}
        doc.render(context)
        doc.save(os.path.join(self.FIXTURE_DIR, 'generated_doc2.docx'))



