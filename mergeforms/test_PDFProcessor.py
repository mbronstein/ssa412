from unittest import TestCase
from .pdfprocessor import  PDFProcessor


class TestPDFProcessor(TestCase):

    pdftk_bin = 'C:\\Program Files (x86)\\PDFtk Server\\bin\\pdftk.exe'
    template_file = '/var/www/lomb/mergeforms/test1.pdf'
    xfdf_file = "C:\\Users\\mark\\AppData\\Local\\Temp\\tmpdjt3brk7 "
    output_file = "C:\\Users\\mark\\projects\\drfx1\\temp\\Vigna_test1_83861.pdf flatten"

    def test_fill_form_(self):
        cmd = "{0} fill_form {1} output {2}".format(self.template_file,
                                                    self.xfdf_file,
                                                    self.output_file
                                                    )
        print("cmd=",cmd)
        self.fail()

