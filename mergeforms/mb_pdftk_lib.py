# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import os
import sys
from tempfile import NamedTemporaryFile

from io import BytesIO

class mbPDFTKException(Exception):
    pass

class FormNotFoundException(mbPDFTKException):
    pass

class FormOutputNotFoundException(mbPDFTKException):
    pass

# wrapper aroud the PDF Toolkit
class mbPDFTK(object):

    def __init__(self,
                 log_filepath=None,
                 output_filepath=None):
        """

        Args:
            source_filepath:
            data_dict_filepath:
            log_filepath:
            output_filepath
        """
        # test for existence of form file?
        self.output_filepath = output_filepath
        self.log_filepath = log_filepath  or "pdftk.log"
        self.cmd = 'pdftk.exe'   # assumes pdftk.exe is accessible. maybe test for it?
        self.pdftk_operation = ""
        self.verbose_flag = True
        # TODO Add other cmds



    def create_executable_command_line_string(self):

        if self.pdftk_operation is None:
            raise Exception("no operation given")
        if self.pdftk_operation == "fill_form":
            cmd_str = "{0} {1} {2} {3} output {4} dont_ask".format(self.cmd,
                                                              self.source_filepath,
                                                              self.pdftk_operation,
                                                              self.data_dict_filepath,
                                                              self.output_filepath)
            if self.verbose_flag:
                cmd_str += ' verbose'
            if self.flatten_flag:
                cmd_str += ' flatten'
            return cmd_str
        elif self.pdftk_operation == "extract_bookmarks":
            self.pdftk_operation = "dump_data"
            cmd_str = "{0} {1} output {2} dont_ask".format(self.cmd,
                                                           self.source_filepath,
                                                           self.pdftk_operation,
                                                           self.output_filepath)

    def run(self):
        arg_str = self.create_executable_command_line_string()
        if self.log_filepath:
            log = open(self.log_filepath,'a+')
        else:
           log = PIPE
        p = Popen(arg_str, stdin=PIPE, stdout=log, stderr=PIPE)
        # p = Popen(arg_str)
        # log.write("args=" + arg_str +'\n')
        # if self.log_filepath:
        #     log.close()
        # if not os.path.exists(self.output_filepath):
        #    raise FormOutputNotFoundException
        return self.output_filepath

    def fill_form(self,
                  source_filepath=None,   #assumes is alread proxyed to local file if a remote URL
                  data_dict_filepath=None,
                  output_filepath = None,
                  flatten=False):
        self.source_filepath = source_filepath
        self.data_dict_filepath = data_dict_filepath
        self.output_filepath = output_filepath or self.output_filepath
        self.pdftk_operation = u'fill_form'
        self.flatten_flag = flatten
        if self.output_filepath is None:
            out_file = NamedTemporaryFile(suffix=".pdf", delete=False)
            self.output_filepath = out_file.name
            out_file.close()
        return self.run()

    def extract_bookmarks(self, source_filepath=None, output_filepath=None):
        self.source_filepath = source_filepath or self.source_filepath
        if self.output_filepath is None:
            out_file = NamedTemporaryFile(suffix=".txt", delete=False)
            self.output_filepath = out_file.name
            out_file.close()
        self.pdftk_operation = u'dump_data'
        if self.output_filepath is None:
            out_file = NamedTemporaryFile(suffix=".txt", delete=False)
            self.output_filepath = out_file.name
            out_file.close()
        return self.run()

    def import_bookmarks(self, source_filepath=None, bookmarks=None, output_filepath=None):
        # NOT DONE
        self.source_filepath = source_filepath or self.source_filepath
        if self.output_filepath is None:
            out_file = NamedTemporaryFile(suffix=".txt", delete=False)
            self.output_filepath = out_file.name
            out_file.close()
        self.pdftk_operation = u'??'
        if self.output_filepath is None:
            out_file = NamedTemporaryFile(suffix=".txt", delete=False)
            self.output_filepath = out_file.name
            out_file.close()
        return self.run()