from unittest import TestCase
from cms10.api_bp.merge_data_extractor import MergeDataExtractor
from flask import Request
from cms10 import create_app
from cms10.settings import DevConfig
from flask_testing import TestCase



class request(object):
    def __init__(self):
        self.method = 'GET'
        self.args = {'claimant': 5101}


class TestMergeDataExtractor(TestCase):

    def setUp(self):
        self.r = request()

    def create_app(self):
        app = create_app(DevConfig)
        return app

    def test_create__merge_data_dic_from_args(self):
        mde = MergeDataExtractor(self.r)
        print mde.get_merge_data_dic()
        self.fail()
