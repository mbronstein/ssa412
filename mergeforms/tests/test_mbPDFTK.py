from ..mb_pdftk_lib import mbPDFTK
import subprocess
import os


testdir_path = os.path.dirname(__file__)

test_form_filename = os.path.join(testdir_path, "mergeforms/mform_test1.pdf")
test_data_filename  =  os.path.join(testdir_path, "mergeforms/test.xfdf")

def test_create_executable_command_line_string():
    p = mbPDFTK(os.path.join(test_form_filename, test_data_filename))

    print(p)
    assert p

    pdf_name = p.fill_form()
    try:
        res = subprocess.Popen('open {0}'.format(pdf_name), shell=True)
    except:
        raise Exception("Error opening pdf: {0}".format(pdf_name))

    assert False



def test_run():
    self.fail()

def test_fill_form(self):


    self.fail()

def test_extract_bookmarks(self):
    self.fail()
