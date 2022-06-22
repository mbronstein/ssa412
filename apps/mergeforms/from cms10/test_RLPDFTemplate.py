from unittest import TestCase, skip
from myapp.api_bp.rlpdftemplate import RLPDFTemplate
from myapp.fixtures.contacts_fixtures import test_context,expected_fields_dic
from collections import OrderedDict
import os
import json

class TestRLPDFTemplate(TestCase):

    def setUp(self):
        self.APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
        self.FIXTURE_DIR = os.path.join(os.path.dirname(self.APP_DIR), 'fixtures')

    @skip
    def test_print_grid_onto_form(self):
        self.fail()

    @skip
    def test_import_form_fields_datadict(self):
        formfp = 'ssa-1695.jpg'
        rlpdf = RLPDFTemplate(formfp, self.FIXTURE_DIR, self.FIXTURE_DIR)
        rlpdf.import_fields_datadic(expected_fields_dic)

        self.assertDictEqual(resultdic, expected_fields_dic)

    @skip
    def test_convert_context_to_form_field_datadict(self):
        formfp = 'ssa-1695.jpg'
        rlpdf = RLPDFTemplate(formfp, self.FIXTURE_DIR, self.FIXTURE_DIR )
        resultdic = rlpdf.convert_context_to_form_field_datadict(test_context)
        self.assertDictEqual(resultdic, expected_fields_dic)

    @skip
    def test_convert_field_defs_json_to_dict(self):
        test_dict_string = "{'contact_first_name':{'x': 1.5, 'y':9,'value':''}, 'contact_last_name':{'x': 1.5, 'y':8.5, 'value': ''},'contact_ssn':{'x': 5.5, 'y':8.5, 'value': ''}}"
        generated_dict = RLPDFTemplate.convert_field_defs_json_to_dict(test_dict_string)
        expected_dict = {
            'contact_first_name': {'x':1.5,  'y':9,   'value': ''},
            'contact_last_name':  {'x':1.5,  'y':8.5,   'value': ''},
            'contact_ssn':        {'x':5.5,   'y': 8.5,  'value': ''}
        }

        self.assertEqual(expected_dict, generated_dict )

    @skip
    def test_import_fields_datadic(self):

        self.fail()

    @skip
    def test_write_fields_onto_form(self):
        self.fail()

    @skip
    def test_create_output_fn(self):
        self.fail()

    @skip
    def test_render(self):
        self.fail()

    @skip
    def test_printgrid(self):
        self.fail()
