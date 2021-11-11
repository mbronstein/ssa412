# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from cms10.settings import Config
import os
import time
from io import BytesIO
import json
from docxtpl import DocxTemplate
from mb_pdftk_lib import PDFTK


class MergeException(Exception):
    """Bass Exception for Merge Related Excleptions"""
    pass

class ContextProcessingException(MergeException):
    pass

class PDFFormMergeError(MergeException):
    pass

class BadFieldDataArguments(MergeException):
    pass

class NonPDFFormError(MergeException):
    pass

class AbstractMergeManager(object):
    """abstract class for manager which imports a base template file and then adds fields on it
    parameters passed in constructor:

        form_filepath (filename of form template)
        output_dirpath(folder created file will go in) # or return as stream
   """
    __metaclass__ = ABCMeta

    def __init__(self, form_filepath=None,
                 form_file=None,
                 form_stream=None,
                 output_stream=None,
                 output_file=None,
                 context=None,
                 field_dic=None):

        # initialize properties not affected by init
        self.outputstream = BytesIO()
        self.field_dic = field_dic
        if context:
            self.import_context_items(context)
        self.doc = None
        # initial properties based on parameters
        self.form_filepath = form_file
        self.form_file = form_file
        self.form_stream = form_stream
        self.output_file = output_file
        self.output_filename = ''
        self.init_form_template()

    @abstractmethod
    def init_form_template(self):
        pass
    
    def import_context_items(self, context):
        """
        import dictionary of fieldname:fieldvalue pairs into self.field_data_dic filteredby nonnull  values
        """
        if context is None:
            return None
        for k, v in context.items():
            if v:
                self.context[k]= v

    # create output filename from form data dic
    def create_output_fn(self):
        if u'contact_last_name' in self.field_data_dic:
            client = self.field_data_dic[u'contact_last_name']
        else:
            client = u'xxx'
        tmplt = u"{0}_{1}_{2}.{3}"
        retval = tmplt.format(client,
                              os.path.splitext(self.form_filename)[0][0:10],
                              time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()),
                              self.mimetype)
        return retval

    @abstractmethod
    def write_fields(self):
        pass

    @abstractmethod
    def save_file(self):
        pass

    def import_field_data_dic(self, dic):
        for item in dic:
            self.field_dic.update(item)


    def convert_context_to_form_field_dic(self, xcontext):
        """assuming context is a dictionarie of objects, combine in an new flat dictoanry
        containing object_field
        """
        retdict = {}
        # for each string key including 'contact', 'fo', .... assign to data_obj
        for key, obj in xcontext.items():
            # for each field  in each data object create field entry with field name and prefix
            for k, v in obj.mergefield_dict().items():
                retdict["{0}_{1}".format(key, k)] = v
        return retdict

    def render(self, field_dic=None, context=None):
        """field_data_dic is already a dictionary of field names which can be imported directly
            context is a dictionary of objects like contact, fo, etc that must be convered to to a dict before importing.
        """
        if field_dic:
            self.import_field_data_dic(field_dic)
        if context: # append to field_data_dict
             context_dic = self.convert_context_to_form_field_dic(context)
             for k in context_dic.keys():
                self.field_data_dic[k] = context_dic[k]

        self.output_filename = self.create_output_fn()
        self.output_filepath = os.path.join(self.output_dirpath, self.output_filename)
        self.write_fields()
        self.save_file()
        return self.output_filepath



class PDFMergeManager(AbstractMergeManager):

    def __init__(self, ????):
        super(PDFMergeManager, self).__init__(????)

    # initialize PTDFTK member with parameters
    def init_form_template(self):
        self.pdftk = PDFTK(self.form_filepath, self.log_filepath) ????


    def write_fields(self):
        self.pdftk.output_filepath = self.output_filepath
        self.pdftk.fill_form(self.field_data_dic)

    def save_file(self):
        # with open(self.output_filepath, 'wb') as f:
        #     self.doc.write(f)
        #     f.close()
        res_fp = self.pdftk.run()
        if res_fp == self.output_filepath:
            return res_fp
        else:
            raise PDFFormMergeError()

class DocxMergeForm(AbstractMergeManager):

    def __init__(self, formfname, form_dirpath, output_dirpath):
        super(DocxMergeForm, self).__init__(formfname, form_dirpath, output_dirpath)
        self.mimetype = 'docx'

    def init_form_template(self):
        self.doc = DocxTemplate(self.form_filepath)

    def write_fields(self):
        self.doc.render(self.field_data_dic)

    def save_file(self):
        self.doc.save(self.output_filepath)

class TemplateLoadError(Exception):
    pass

def template_factory(formfname, form_dirpath, output_dirpath, field_defs=None):
    """create proper subclass of AbstractMergeTemplate vased on extension of form file"""
    if os.path.splitext(formfname)[1] in ['.pdf', '.jpg', '.tif']:
        tmplt = PDFMergeForm(formfname, form_dirpath, output_dirpath)
    elif os.path.splitext(formfname)[1] in ['.doc', '.docx']:
        tmplt = DocxMergeForm(formfname, form_dirpath, output_dirpath)
    else:
        raise TemplateLoadError
    return tmplt





                # def render_grid(self):
    #     # print a grid on form.
    #
    #     def write_grid_coordinates():
    #         '''
    #         put grid coordinates on form to use to locate fields
    #         '''
    #         for x in numpy.arange(.5, 11, .5):
    #             for y in numpy.arange(11, 1, -.5):
    #                 self.doc.setFontSize(9)
    #                 self.doc.drawString(x * inch, y * inch, '({0}",{1})"'.format(x, y))
    #                 # self.imgDoc.drawString(y * inch, x * inch, '({0}",{1})"'.format(y,x))
    #         self.doc.save()
    #
    #     write_grid_coordinates()
    #     self.output_filename = "{0}_{1}_{2}.{3}".format('grid',
    #                                                     os.path.splitext(self.form_filename)[0][0:10],
    #                                                     time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()),
    #                                                     self.mimetype)
    #     self.output_filepath = os.path.join(self.output_dirpath, self.output_filename)
    #     self.save_file()
    #     return self.output_filepath
    #

# class PDFMergeFormwithReportlab(AbstractMergeTemplate):
#
#     def __init__(self, formfname, form_dirpath, output_dirpath, field_defs):
#         super(PDFMergeForm, self).__init__(formfname, form_dirpath, output_dirpath, field_defs)
#         self.mimetype = 'pdf'
#
#
#     def init_form_template(self):
#
#         #if template is an image file use reportlab to create the form ortherwise use pypdf2
#         fn, ext  = os.path.splitext(self.form_filename)
#         self.doc =  Canvas(self.outputstream, pagesize=letter)
#         if ext == '.pdf':
#             self.init_pdf_form_from_pdf_file()
#         elif ext in ['.jpg', '.tif', '.tiff', '.png']:   # what happens if multipage tif?
#             # draw image of form on Canvas.
#             self._init_pdf_form__from_imagefile()
#         else:
#             raise BadFieldDataArguments
#
#     def _init_pdf_form__from_imagefile(self):
#         # create output reportlab canvas connected to Stream object:
#         self.doc = Canvas(self.outputstream, pagesize=letter)  #reportlab canvas linked to self.outputstream
#         # Draw the form image on Canvas
#         self.doc.drawImage(self.form_filepath, 0, 0, 8.5 * inch, 11 * inch)
#
#     def init_pdf_form_from_pdf_file(self):
#         # create output reportlab canvas connected to Stream object:
#         self.doc = Canvas(self.outputstream)
#         # read pages from source pdf file and add each to  canvas bject
#         pages = PdfReader(self.form_filepath).pages
#         pages = [pagexobj(x) for x in pages]
#
#         for page in pages:
#                 self.doc.setPageSize((page.BBox[2], page.BBox[3]))
#                 self.doc.setPageSize((612, 792))
#                 self.doc.doForm(makerl(self.doc, page))
#                 self.doc.showPage()
#
#     def write_fields(self, font='Helvetica', size=10):
#         #write fields onto Reportlab Canvas conaining form
#
#         self.doc.setFont(font, size)
#         for k,ff in self.field_defs_dic.items():
#             x = "{0}".format(ff.value)
#             self.doc.drawString(ff.x * inch, ff.y * inch, "{0}".format(ff.value))
#
#     def save_file(self):
#         #save canvas and then save outputstream to self.output_filepath
#         self.doc.save()
#         with open(self.output_filepath, 'wb') as f:
#             f.write(self.outputstream.getvalue())
#             f.close()
#
#     def render_grid(self):
#         #print a grid on form.
#
#         def write_grid_coordinates():
#             '''
#             put grid coordinates on form to use to locate fields
#             '''
#             for x in numpy.arange(.5, 11, .5):
#                 for y in numpy.arange(11, 1, -.5):
#                     self.doc.setFontSize(9)
#                     self.doc.drawString(x * inch, y * inch, '({0}",{1})"'.format(x, y))
#                     # self.imgDoc.drawString(y * inch, x * inch, '({0}",{1})"'.format(y,x))
#             self.doc.save()
#
#         write_grid_coordinates()
#         self.output_filename = "{0}_{1}_{2}.{3}".format('grid',
#                                           os.path.splitext(self.form_filename)[0][0:10],
#                                           time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()),
#                                           self.mimetype)
#         self.output_filepath = os.path.join(self.output_dirpath, self.output_filename)
#         self.save_file()
#         return self.output_filepath
#
