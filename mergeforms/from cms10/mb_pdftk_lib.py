# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import os
import sys
from tempfile import mkdtemp, mkstemp, NamedTemporaryFile

# import fdfgen
from io import BytesIO

class PDFTKException(Exception):
    pass

class FormNotFoundException(PDFTKException):
    pass

class FormOutputNotFoundException(PDFTKException):
    pass
# wrapper aroud the PDF Toolkit
class PDFTK(object):

    def __init__(self, form_filepath, log_filepath = None):
        # test for existence of form file?
        if not os.path.exists(form_filepath):
            raise FormNotFoundException
        self.form_filepath = form_filepath
        if not os.path.exists(self.form_filepath):
            raise FormNotFoundException
        self.output_filepath = ""
        self.log_filepath = log_filepath
        self.cmd = u'pdftk.exe'   # assumes pdftk.exe is accessible. maybe test for it?
        self.pdftk_operation = ""
        self.context = {}
        self.flatten_flag = False
        self.verbose_flag = True
        self.xfdf_string = ''
        self.xfdf_filepath = ''
        self.tempdir = mkdtemp()

    def create_executable_command_line_string(self):
        # args =  [ self.cmd,
        #           self.form_filepath,
        #           self.pdftk_operation,
        #           self.xfdf_filepath,
        #           "output",
        #           self.output_filepath,
        #           'dont_ask'
        #           ]
        args = "{0} {1} {2} {3} output {4} dont_ask".format(self.cmd,
                                                              self.form_filepath,
                                                              self.pdftk_operation,
                                                              self.xfdf_string,
                                                              self.output_filepath)
        if self.verbose_flag:
            args += ' verbose'

        if self.flatten_flag:
            args += ' flatten'
        return args

    @staticmethod
    def data_dict_to_xfdf_string(self, data_dict, **kwargs):

        """convert dictionary to xfdf file

        Arguments:
            datdict:
            **kwargs:
        Returns: string
        """

        xfdf_template='<?xml version="1.0" encoding="UTF-8" ?>' + \
        '<xfdf xmlns="http://ns.adobe.com/xfdf/" xml:space="preserve"><fields>' + \
        '{0}</fields>/</xfdf>'

        fld_list_as_xml = ""
        for k in data_dict:
            if data_dict.get(k, None):
                fld_list_as_xml += "<field>{0}</field>".format(data_dict.get(k, None))
        for k in kwargs:
            if data_dict.get(k, None):
                fld_list_as_xml += "<field>{0}</field>".format(data_dict.get(k, None))
        return xfdf_template.format(fld_list_as_xml)


    def temp_file_from_string(self, str, dir=None):
        temp_file = NamedTemporaryFile(dir=dir)
        with open(temp_file, "w" as f:
            f.write(str)
        return temp_file




        f = open(fpath,'wb')
        w = XMLWriter(f)
        w.__encoding = 'utf-8'
        w.declaration()
        w.start('xfdf', xmlns="http://ns.adobe.com/xfdf/")
        w.start('fields')
        for k, v in self.data_dic.items():
            w.start('field', name=k)
            w.start('value')
            w.data( v)
            w.end('value')
            w.end('field')
        w.end('fields')
        w.end('xfdf')
        return fpath

    def fill_form(self, dic, **kwargs):
        self.pdftk_operation = u'fill_form'
        self.data_dic = dic
        self.data_dic.update(kwargs)
        self.xfdf_filepath =  os.path.splitext(self.output_filepath)[0] + '.xfdf'
        self.create_xfdf_file(self.xfdf_filepath)

    def extract_bookmarks(self):
        self.pdftk_operation = u'dump_data'

    def run(self):
        arg_str = self.create_exec_args_string()
        if self.log_filepath:
            log = open(self.log_filepath,'a+')
        else:
            log = PIPE
        p = Popen(arg_str, stdin=PIPE, stdout=log, stderr=PIPE)
        log.write("args=" + arg_str +'\n')
        print(arg_str)
        if self.log_filepath:
            log.close()
        # if not os.path.exists(self.output_filepath):
        #    raise FormOutputNotFoundException
        return self.output_filepath

    """
    <?xml version="1.0" encoding="UTF-8" ?>
<xfdf xmlns="http://ns.adobe.com/xfdf/" xml:space="preserve">
  <fields>
    <field name="ACombo"><value>Red</value></field>
  </fields>
  <annots>
    <square subject="Rectangle" page="0" rect="306.01,744.85,408.98,775.94" flags="print" name="447c49b7-5e50-4b13-adc8-c291102466e6" title="Guest" date="D:20171226120150-08'00'" color="#000000" width="5" creationdate="D:20171226120147-08'00'">
      <popup flags="print,nozoom,norotate" page="0" rect="0,767,112.5,842" open="no"/>
    </square>
  </annots>
</xfdf>"""