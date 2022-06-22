import pytest
from ..pdfprocessor import PDFProcessor

import os
import time


@pytest.fixture
def fld_dict():
    return {
        'claimant.last_name': 'Jones',
        'claimant.first_name': 'John',
        'claimant.full_name': 'John Jones',
        'claimant.birth_date': '04/21/1953',
        'claimant.ssn': '111-22-1234',
        'claimant.address1': '9 Pine St.',
        'claimant.address2': 'Apt 2',
        'claimant.city': 'Boston',
        'claimant.state': 'MA',
        'claimant.zipcode': '02466',
        'claimant.city_state_zip': 'Boston, MA 02466',
        'ssoffice:.address': '19 Radcliff Dr',
        'ssoffice:.city': 'Boston',
        'ssoffice:.state': 'MA',
        'ssoffice:.zipcode': '02111',
        'key1': 'val1'
    }


fixture_dir = os.path.abspath('fixtures')


def test_form_file_exists():
    form_file = os.path.join(fixture_dir, "test1.pdf")
    assert os.path.exists(form_file)


def test_a_field_dict_exists():
    field_dict_file = os.path.join(fixture_dir, "context.json")


# def test_flatten_dict_to_dict_list(a_context_dict):
#     d= a_context_dict
#     x = flatten_dict_to_dict_list(d)
#     assert x == lst1

def test_data_dict_to_xfdf_as_string(a_context_dict):
    d = a_context_dict
    pdftk = PDFProcessor()
    x = pdftk.create_xfdf_file(d)
    assert x


def test_data_dict_to_xfdf_as_file(a_context_dict):
    d = a_context_dict
    pdftk = PDFProcessor()
    x = pdftk.create_xfdf_file(d, to_file=True)
    assert os.path.exists(x)


def test_form_fill(a_context_dict):
    templatefp = os.path.join(fixture_dir, "test1.pdf")

    t = time.localtime()
    s = str(t.tm_hour * 3600 + t.tm_min * 60 + t.tm_sec)
    output_fp = os.path.join(fixture_dir, "output" + s + ".pdf")

    p = PDFProcessor()
    x = p.fill_form_(source_fp=templatefp,
                     context_dict=a_context_dict,
                     output_fp=output_fp
                     )
    assert x
