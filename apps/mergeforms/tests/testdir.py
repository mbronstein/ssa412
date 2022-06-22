import os
from pathlib import Path


def testdir1():
        s = 'C:/Users/mark/projects/drfx1/mergeforms/tests/mbform_test1.pdf'
        formp = Path("c:/users/mark/projects / drfx1 / mergeforms / tests / mbfor_test1.pdf")
        formp1 = Path('mform_test1.pdf')
        os.path.exists(str(formp1))

        assert formp.exists()



def test_form_fill( a_context_dict):
        testdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


        d ={"contact":{"last_name": "Bronstein"}}
        pdfp = PDFProcessor()
        pdf_name = pdfp.fill_form_(source_file_url = frm, context=a_context_dict)
        assert pdf_name
