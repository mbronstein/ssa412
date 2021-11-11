from unittest import TestCase, skip
from cms10.settings import Config
from .mb_pdftk_lib import PDFTK
import os
import time



class TestPDFTK(TestCase):


    def setUp(self):


        self.APP_DIR = Config.APP_DIR
        self.FORM_DIR = os.path.abspath(os.path.join(self.APP_DIR, 'static', 'formlib'))
        self.FIXTURE_DIR = os.path.join(self.APP_DIR, 'fixtures')
        self.OUTPUT_DIR = os.path.join(self.FIXTURE_DIR, 'output')

        self.data_dic = {"claimant_address_lines": "19 Radcliff Drive",
                 "claimant_full_name": "John Smith",
                 "claimant_first_name": "John",
                 "claimant_last_name": "Smith",
                 "claimant_middle_name": "Michael",
               "claimant_birthdate": "04/21/1953",
               "claimant_ssn":"011-22-2222",
               "claimant_city": "Boston",
               "claimant_state": "MA",
               "claimant_zipcode": "02110",
               "claimant_city_state_zipcode":"Boston, MA  02110",
               "form_date": "10/01/2016"}

    # @skip
    # def test_merge1(self):
    #     """test pdftk merge with existing form and existing xfdf exported by acrobat"""
    #     formname = '827.pdf'
    #     xfdfname = '827data.xfdf'
    #     fp = os.path.join(self.FIXTURE_DIR, formname)
    #     log_filepath = os.path.join(self.FIXTURE_DIR, 'merge_log.txt')
    #     pdftk = PDFTK(fp,log_filepath)
    #     pdftk.xfdf_filepath = os.path.join(self.FIXTURE_DIR, xfdfname)
    #     pdftk.output_filepath = os.path.join(self.FIXTURE_DIR, '827out_1' + 'pdf')
    #     pdftk.run()

    def test_merge2(self):
        """test pdftk merge with existing form and generated xfdf file"""
        formname = 'ssa-1696-form.pdf'
        fp = os.path.join(self.FORM_DIR, 'ss', formname)
        log_filepath = os.path.join(self.OUTPUT_DIR, 'merge_log.txt')
        pdftk = PDFTK(fp, log_filepath)
        dt_string = time.strftime("%Y%m%d%H%M%S")
        out_filename = "out_" + dt_string + ".pdf"
        pdftk.output_filepath = os.path.join(self.OUTPUT_DIR, out_filename)
        pdftk.fill_form(self.data_dic)
        pdftk.run()
