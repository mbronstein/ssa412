from unittest import TestCase
from contacts.wip.aws_utils import mbAWSManager
import os
from configparser import ConfigParser


def setAwsCredentials():
    config = ConfigParser()
    config.read(os.path.join(os.path.expanduser("~"), ".aws/credentials"))
    return config.get("default", "aws_access_key_id"), config.get("default", "aws_secret_access_key")


class TestMbAWSManager(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.aws_access_key_id, cls.aws_secret_access_key = setAwsCredentials()

    def setUp(self):
        pass

    def test_getAwsCredentials(self):
        awsm = mbAWSManager()
        self.assertIsNotNone(awsm, "ombawsmanager not imported from .aws")
        self.assertTrue(awsm.key_secret, "key_secret not imported from .aws")
        self.assertTrue(awsm.key_id, "key_id not created")
        awsm = None
        awsm = mbAWSManager(key_id="mykeyid", key_secret="mykeysecret")
        self.assertEqual(awsm.key_id, "mykeyid", msg="key_id not set")
        self.assertEqual(awsm.key_secret, "mykeysecret", msg="key_secret not set")

    def test_get_auth_token(self):
        awsm = mbAWSManager()
        calc_token = awsm.get_auth_token()
        self.assertEqual(calc_token, "AWS " + self.aws_access_key_id + ":" + self.aws_secret_access_key,
                         "calculated autht oken wrong")

    def test_get_bucket(self):
        awsm = mbAWSManager(bucket="lomb_forms")
        buck = awsm.get_bucket()
        self.assertEqual(buck, "lomb_forms", "error setting and reading bucket")

    def test_get_file_obj(self):
        awsm = mbAWSManager(bucket="lomb_forms")
        f_body = awsm.get_file("lomb-forms", "sample.pdf")
        self.assertIsNotNone(f_body, "no file returned")

        with open("test.pdf", 'wb') as output:
            output.write(f_body)
        print('done')


    def test_get_file_list(self):
       awsm = mbAWSManager(bucket='lomb-forms')
       lst = awsm.get_file_list()
       print(lst)
