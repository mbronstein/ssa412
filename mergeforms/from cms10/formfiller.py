from  pypdftk import fill_form
from mergeforms.models import  MergeForm
from mergeforms.utils import

class FormFillerException(Exception):
    pass

class FormFiller:
    """takes form and contact data and renders"""

    def __init__(self, frm_file_path=None, context=None):
        """
        Args:
            frm_file:
            context:

        Returns:
            ?
        """

        self.frm_file_path = frm_file_path or None
        self.context = context or {}



    def render_(self, frm_file_path=None, context=None, format=None, *args, **kwargs):
        pass



    # def render_from_form_as_stream(self, template_type, form_str, fields_dic):
    #     try:
    #             return fill_form(form_str)
    #         elif template_type == 'docx':
    #             return '?'
    #         elif template_type == 'reportlaw':
    #             return '?'
    #         else:
    #             pass
    #
    #     except:
    #         raise (FormRenderException)
    #
    #     def to_field_dic(prefix, dic):
    #         fld_dic = {}
    #         for k in dic.keys():
    #             dic[prefix + '_' + k] = dic[k]
    #         return fld_dic
    #
    #     def render_pdf_mform(self, form_path=None, form_stream=None, field_data_dic=None):
    #


