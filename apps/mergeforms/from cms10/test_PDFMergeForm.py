from unittest import TestCase, skip
from abstract_merge_template import PDFMergeForm
import os


class TestPDFMergeForm(TestCase):

    def setUp(self):
        self.APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
        self.FIXTURE_DIR = os.path.join(os.path.dirname(self.APP_DIR), 'fixtures')

        self.datadic = {}
        self.datadic['contact_last_name'] = 'Jones'
        self.datadic['contact_first_name'] = 'John'
        self.datadic['contact_full_name'] = 'John Jones'
        self.datadic['contact_birth_date'] = '04/21/1953'
        self.datadic['contact_ssn']   = '111-22-1234'
        self.datadic['contact_address1'] = '9 Pine St.'
        self.datadic['contact_address2'] = 'Apt 2'

        self.datadic['contact_city'] = 'Boston'
        self.datadic['contact_state'] = 'MA'
        self.datadic['contact_zipcode'] = '02466'
        self.datadic['contact_city_state_zip'] = 'Boston, MA 02466'




    @skip
    def test_init_form_template(self):

        self.fail()

    @skip
    def test__init_pdf_form__from_imagefile(self):
        self.fail()

    @skip
    def test_init_pdf_form_from_pdf_file(self):
        self.fail()

    @skip
    def test_save_file_and_return(self):
        self.fail()

    @skip
    def test_write_fields(self):
        self.fail()

    @skip
    def test_write_grid_coordinates(self):
        self.fail()

    def test_render_grid(self):
        frm = PDFMergeForm("ssa-1696-form.jpg", self.FIXTURE_DIR, self.FIXTURE_DIR )
        frm.render_grid()

