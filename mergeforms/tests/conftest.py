import pytest

@pytest.fixture
def a_contact_dict():
    return {
        'contact_last_name':'Jones',
        'contact_first_name':'John',
        'contact_full_name':'John Jones',
        'contact_birth_date':'04/21/1953',
        'contact_ssn':'111-22-1234',
        'contact_address1':'9 Pine St.',
        'contact_address2':'Apt 2',
        'contact_city': 'Boston',
        'contact_state':'MA',
        'contact_zipcode':'02466',
        'contact_city_state_zip':'Boston, MA 02466'
    }




@pytest.fixture
def a_context_dict():
    return {
         'contact': {
            'last_name':'Jones',
            'first_name': 'John',
            'full_name': 'John Jones',
            'birth_date': '04/21/1953',
            'ssn': '111-22-1234',
            'address1': '9 Pine St.',
            'address2': 'Apt 2',
            'city': 'Boston',
            'state': 'MA',
            'zipcode': '02466',
            'city_state_zip': 'Boston, MA 02466'
        },
        'ssoffice:': {
            'address':'19 Radcliff Dr',
            'city': 'Boston',
            'state': 'MA',
            'zipcode': '02111'
        },
        "key1":"val1",
    }
