
import os
import numpy
import time
from reportlab.pdfgen import canvas
from io import BytesIO

from docxtpl import DocxTemplate

class BadFieldDataArguments(Exception):
    pass

class WordTemplate(object):
    """
    template based on MSWord docx
    """

    def __init__(self, formfname, form_dirpath, output_dirpath=None):

        self.formname = None
        self.outputstream = BytesIO()
        self.field_defs_dic = {}
        self.form_filename = formfname
        self.formfile_ext = 'docx'
        self.form_dirpath = form_dirpath
        self.form_filepath = os.path.join(self.form_dirpath, self.form_filename)
        self.output_dirpath = output_dirpath
        #set up a reportlab doc linked to a outputstream
        self.doc = DocxTemplate(self.form_filepath)

    def convert_context_to_form_field_datadict(self, xcontext):
        """
        assuming context is a dictionarie of objects, combine in an new dictionary
        containing ...
        """
        retdict = {}
        for key, obj in xcontext.items():  # for each string key including 'contact', 'fo', .... assign to data_obj
            # for each field  in each data object create field entry with field name and prefix
            for k, v in obj.mergefield_dict().items():
                retdict["{0}_{1}".format(key, k)] = v
                # add field for city state zip line in forms
        if retdict.has_key("contact_city"):
            retdict["contact_city_state_zip"] = \
                "{0}, {1}  {2}".format(retdict['contact_city'], retdict['contact_state'], retdict['contact_zipcode'])
        return retdict

    def import_fields_datadic(self, dic):
        """
        for each key in self.field_defs_dic,
           if key exists in dic, imporit its value
         value

        """
        for k,v in self.field_defs_dic.items():
            if dic.has_key(k):
                self.field_defs_dic[k]['value'] = dic[k]

    def create_output_fn(self):
        if self.field_defs_dic.has_key('contact_last_name'):
            client = self.field_defs_dic['contact_last_name']['value']
        else:
            client = 'xxx'
        retval = "{0}_{1}_{2}.{3}".format(client,
                                          os.path.splitext(self.form_filename)[0][0:10],
                                          time.strftime("%H-%M-%S", time.localtime()),
                                          self.formfile_ext)
        return retval




    def render(self, fielddic=None, context=None):
        """parameters fielddic and context are alternatives. cnat be both or neither
            fielddic is already a dictionary of fieldnamees which can be imported directly
            context is a dictionary of objects like contact, fo, etc that must be convered to to a dict before importing.
        """

        if  (fielddic and context):
            raise BadFieldDataArguments

        if fielddic:
            self.import_fields_datadic(fielddic)
            self.output_filename = self.create_output_fn()
            self.output_filepath = os.path.join(self.output_dirpath, self.output_filename)
            self.doc.save()  #needed to finalize the new form

        elif context:
            fielddic = self.convert_context_to_form_field_datadict(context)
            self.import_fields_datadic(fielddic)
            self.output_filename = self.create_output_fn()
            self.output_filepath = os.path.join(self.output_dirpath, self.output_filename)
        else:
            pass

        self.doc.save(self.output_filepath)
        return self.output_filepath

