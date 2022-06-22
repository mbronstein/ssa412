
import os
import numpy
import time
from abstract_merge_template import AbstractMergeTemplate, BadFieldDataArguments
from reportlab.pdfgen import canvas
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import inch
import json


class MergeFieldDef(object):
    def __init__(self, name, value, x, y):
        self.name = None
        self.value = None
        self.x = None
        self.y = None


class RLPDFTemplate(AbstractMergeTemplate):
    """template based on reportlab which imports an image file and then adds fields on it"""

    def __init__(self, formfname, form_dirpath, output_dirpath=None, field_defs_dic=None):
        self.field_defs_dic = self.set_field_defs_dic(field_defs_dic)
        super(RLPDFTemplate, self).__init__(formfname, form_dirpath, output_dirpath)
        self.formfile_ext = 'pdf'
        #set up a reportlab doc linked to a outputstream
        self.imgDoc = canvas.Canvas(self.outputstream,pagesize=letter)
        # Draw the form image on Canvas and save it to the pdf in buffer
        self.imgDoc.drawImage(self.form_filepath, 0,0, 8.5*inch, 11*inch)

    def convert_field_defs_json_to_dict(s_dict):
        """
             take string string containing field defs and convert to
             python dict and add to template object
             (this would be used if field defs are stored in a string field as json dictionary.)
        """
        try:
            d = json.loads(s_dict)
            return d
        except Exception as e:
            print(e.message, e.args)

    def set_field_defs_dic(self, field_defs=None):
        if field_defs is None:
            return None
        for k in field_defs.keys():
            fld_def = field_defs[k]
            self.field_defs_dic[k] = {}
            self.field_defs_dic[k][u'name'] = fld_def.name
            self.field_defs_dic[k][u'x'] = fld_def.x
            self.field_defs_dic[k][u'y'] = fld_def.y
            self.field_defs_dic[k][u'value'] = ''
            self.field_defs_dic[k][u'page'] = fld_def.page

    def print_grid_onto_form(self):
        for x in numpy.arange(.5, 11,.5):
            for y in numpy.arange(11,1,-1):
                self.imgDoc.setFontSize(9)
                self.imgDoc.drawString(x * inch, y * inch, '({0}",{1})"'.format(x,y))
                # self.imgDoc.drawString(y * inch, x * inch, '({0}",{1})"'.format(y,x))




    def write_fields_onto_form(self):
        self.imgDoc.setFontSize(10)
        for k,v in self.field_defs_dic.items():
            self.imgDoc.drawString(v['x'] * inch, v['y'] * inch, "{0}".format(v['value']))


    def render(self, fielddic=None, context_dic=None):
        """parameters fielddic and context are alternatives. cnat be both or neither
            fielddic is already a dictionary of fieldnamees which can be imported directly
            context is a dictionary of objects like contact, fo, etc that must be convered to to a dict before importing.
        """

        if (fielddic and context_dic):
            raise BadFieldDataArguments

        if fielddic:
            self.import_fields_datadic(fielddic)
            self.output_filename = self.create_output_fn()
            self.output_filepath = os.path.join(self.output_dirpath, self.output_filename)
            self.write_fields_onto_form()
            self.imgDoc.save()  #needed to finalize the new form

        elif context_dic:
            fielddic = self.convert_context_to_form_field_datadict(context_dic)
            self.import_fields_datadic(fielddic)
            self.output_filename = self.create_output_fn()
            self.output_filepath = os.path.join(self.output_dirpath, self.output_filename)
            self.write_fields_onto_form()
            self.imgDoc.save()

        else:  # no context or field dic return blank form
            self.output_filename = self.create_output_fn()
            self.output_filepath = os.path.join(self.output_dirpath, self.output_filename)
            self.imgDoc.save()

        with open(self.output_filepath, 'wb') as f:
            f.write(self.outputstream.getvalue())
            f.close()
        return self.output_filepath


    def printgrid(self):
        """prints the imported form plus a superimposed grid"""
        self.output_filename = self.create_output_fn()
        self.output_filepath = os.path.join(self.output_dirpath, self.output_filename)
        self.write_fields_onto_form()
        self.print_grid_onto_form()
        self.imgDoc.save()

        with open(self.output_filepath, 'wb') as f:
            f.write(self.outputstream.getvalue())
            f.close()
        return self.output_filepath



class SSA1695Template(RLPDFTemplate):
    def __init__(self,form_dirpath, output_dirpath=None):
        super(SSA1695Template,self).__init__( 'ssa-1695.jpg', form_dirpath, output_dirpath)
        self.formname='ssa-1695'
        self.field_datadic ={
            'contact_first_name':  {'basename':'first_name','x': 1.5, 'y':9,   'value': None},
            'contact_last_name':   {'basename':'last_name','x': 1.5, 'y':8.5, 'value': None},
            'contact_ssn':         {'basename':'ssn','x': 5.5, 'y':8.5, 'value': None}
            # 'contact_birthdate': {'basename':birthdate,'x':0,   'y':0,'value':None},
            # 'contact_address1':  {'basename':address1,'x':0,   'y':0,'value':None},
            # 'contact_city':      {'basename':None,'x':0,   'y':0,'value':None},
            # 'contact_state':     {'basename':None,'x':0,   'y':0,'value':None},
            # 'contact_zipcode':   {'basename':None,'x':0,   'y':0,'value':None},
            # 'contact_home_phone':{'basename':None,'x':0,   'y':0,'value':None}
        }


class SSA1696Template(RLPDFTemplate):
    def __init__(self,  form_dirpath, output_dirpath=None):
        super(SSA1696Template, self).__init__("ssa-1696-form.jpg", form_dirpath, output_dirpath)
        self.formname = 'ssa-1696'
        self.field_defs_dic = {
            'contact_full_name': {'basename': 'full_name', 'x': 1, 'y': 10.1, 'value': ""},
            # 'contact_last_name':  {'basename': 'last_name', 'x': 1.5, 'y': 8.5, 'value': ""},
            'contact_ssn':        {'basename': 'ssn', 'x': 4.5, 'y': 10.1, 'value': ""},
            # 'contact_birthdate':  {'basename': 'birthdate','x':0,   'y':0,'value':""},
            'contact_address1':   {'basename': 'address1','x':4.8,   'y':7.2,'value':""},
            'contact_address2':   {'basename': 'address2', 'x': 5.6, 'y': 7.2, 'value': ""},
            'contact_city_state_zip':       {'basename': 'city_state_zip','x':4.8,   'y':7.0,'value':""},
            # 'contact_state':      {'basename': 'state','x':0,   'y':0,'value':""},
            # 'contact_zipcode':    {'basename': 'zipcode','x':0,   'y':0,'value':""}
            # 'contact_home_phone':{'basename':None,'x':0,   'y':0,'value':""}
        }

class SSA827Template(RLPDFTemplate):
    def __init__(self,  form_dirpath, output_dirpath=None):
        super(SSA827Template, self).__init__("ssa-1696-form.jpg", form_dirpath, output_dirpath)
        self.formname = 'ssa-827'
        self.field_defs_dic = {
            'contact_full_name': {'basename': 'full_name', 'x': 1, 'y': 10.1, 'value': ""},
            # 'contact_last_name':  {'basename': 'last_name', 'x': 1.5, 'y': 8.5, 'value': ""},
            'contact_ssn':        {'basename': 'ssn', 'x': 4.5, 'y': 10.1, 'value': ""},
            # 'contact_birthdate':  {'basename': 'birthdate','x':0,   'y':0,'value':""},
            'contact_address1':   {'basename': 'address1','x':4.8,   'y':7.2,'value':""},
            'contact_address2':   {'basename': 'address2', 'x': 5.6, 'y': 7.2, 'value': ""},
            'contact_city_state_zip':       {'basename': 'city_state_zip','x':4.8,   'y':7.0,'value':""},
            # 'contact_state':      {'basename': 'state','x':0,   'y':0,'value':""},
            # 'contact_zipcode':    {'basename': 'zipcode','x':0,   'y':0,'value':""}
            # 'contact_home_phone':{'basename':None,'x':0,   'y':0,'value':""}
        }



