import os
import subprocess
import time
from tempfile import mkdtemp, NamedTemporaryFile

import requests


# === utilities used in class ===
#   TODO: later may be moved to another module

def unique_filename(prefix=None, suffix=None):
    return "{0}{1}{2}".format(prefix, time_in_seconds_str(), suffix)


def time_in_seconds_str():
    """return time in seconds since midnight local time"""
    t = time.localtime()
    return str(t.tm_hour * 3600 + t.tm_min * 60 + t.tm_sec)


def local_proxy_for_remote_file(file_uri, prefix=None, suffix=None):
    """
    Retrieve contents of remote file and save to a local file for further processing
    Args:
        file_uri:
        prefix:
        suffix

    Returns:
        file_path as string
    """
    temp_file = ""
    try:
        file_body = requests.get(file_uri)
    except Exception as e:
        raise Exception("Error retrieving {0}: {1}".format(file_uri.name, str(e)))
    try:
        temp_file = NamedTemporaryFile(delete=False, prefix=prefix, suffix=suffix)
        temp_file.write(file_body)
        temp_file.close()
        return temp_file.name
    except Exception as e:
        raise Exception("Error saving {0}: {1}".format(temp_file.name, str(e)))


def test_if_file_is_local_and_if_not_create_proxy(file_url):
    fn = file_url
    if file_url.upper().startswith("HTTP"):
        fn = local_proxy_for_remote_file(file_url)
        print("fn", fn)
        print("abspath:", os.path.abspath(fn))
        print("checkvalue:", '\\users\\mark\\projects\\drfx1\\mergeforms\\tests\\mform_test1.pdf')
        print("equals?:", fn == '\\users\\mark\\projects\\drfx1\\mergeforms\\tests\\mform_test1.pdf')

    # elif not os.path.exists(fn):
    #     raise PDFFormFillerException("error opening template file: {0}".format(fn))
    else:
        return fn


def flatten_dict( context_dict: dict):
    """
        turn dict (optionally nested) into flat dict
        if dict value is a string, put dict in destination dict as is,
        if dic value is another dict, preface each key with the name of the parent dic and then transfer.

        TODO: maybe add code to allow list param and process that as well and not assume each item is a dict.
           so 1) test variable, if dict, process as potentially nested dict, and use key as parent node.
            2) if list process each list item and if dic process as above with no prefix

        Args:
            context:dict:

        Returns:
           dict
        """
    flat_dict = {}
    # for each key  in the source context dictionary(eg  'claimant', 'matter','contact', 'fo', fldname ),
    # assign key to context_key

    for context_key in context_dict:
        # if value referenced by the dictionary key  is a dict...
        if isinstance(context_dict[context_key], dict):
            # add the actual dictionary for look up purposes by template
            # flat_dict[context_key] = context[context_key]    #todo: removed this .  replace if needed

            # add the members into the top level of the dict with namespaced fieldnames
            namespace = context_key + "."
            # assume each item in the list is a keyword-value pair
            # for each dic in list, add prefix to keyword and add pair to list to be returned
            for k in context_dict[context_key]:  # for each dic key in the list
                flat_dict[namespace + k] = context_dict[context_key][k]
        elif isinstance(context_dict[context_key], str):
            flat_dict[context_key] = context_dict[context_key]
        elif type(context_dict[context_key]).__name__ == "list":
            # TODO: handle nested list of dictionaries, like in phones, or emails, or docs or matters (or not nec?)
            raise Exception("sublist found.  Don't know how to process nexted sublist")
        else:
            raise Exception(
                "Item may be a {0}.Since it is neither a dict or a string. Dont know how to process".format(
                    type(context_dict[context_key].__name__)))
        return flat_dict


# =====end of Utilities section =========

class PDFProcessorException(Exception):
    pass


class PDFProcessor:
    """process a form template and a dictionary (context) to create a merged doc

        """

    def __init__(self,
                 log_filepath=None,
                 pdftk_bin=None,
                 ):
        """
        Args:
            log_filepath: str
            pdftk_bin: str
        """
        self.pdftk_bin = pdftk_bin or "C:\\Program Files (x86)\\PDFtk\\bin\\pdftk.exe"
        self.log_filepath = log_filepath or os.path.join(os.path.dirname(__file__), "pdftk.log")


    def create_xfdf_file(self, context_dict=None, to_file=True, xfdf_fp=None):
        # TODO add some try excepts
        xfdf_template_str = '<?xml version="1.0" encoding="UTF-8" ?>' + \
                            '<xfdf xmlns="http://ns.adobe.com/xfdf/" xml:space="preserve"><fields>' + \
                            '{0}</fields>/</xfdf>'

        field_template_str = '<field name="{0}"><value>{1}</value></field>'

        fld_list_as_xml = ""
        flattened_dict = flatten_dict(context_dict=context_dict)
        # convert flat dictlist to xfdf body
        for k in flattened_dict:
                fld_list_as_xml += field_template_str.format(k, flattened_dict[k])
        xfdf_body = xfdf_template_str.format(fld_list_as_xml)
        if to_file is False:
            return xfdf_body
        else:
            fp = xfdf_fp or os.path.join(mkdtemp(), unique_filename(suffix=".xfdf"))
            with open(fp, 'w') as f:
                f.write(xfdf_body)
            return fp


    def create_pdftk_arg_string(self,
                                cmd=None,
                                source_fp=None,
                                data_fp=None,
                                output_fp=None):

        arg_str_templates = {"fill_form": "{source_fp} fill_form {data_fp} output {output_fp}",
                             "extract_bookmarks": "??",
                             }
        arg_str_template = arg_str_templates.get(cmd, None)
        if not arg_str_template:
            raise PDFProcessorException("{0} not recognized as pdftk command".format(cmd))
        else:
            arg_str = arg_str_template.format(source_fp=source_fp,
                                              data_fp=data_fp,
                                              output_fp=output_fp
                                              )
        return arg_str

    def run_pdftk_bin(self, arg_string):

        cmd_str = self.pdftk_bin + " " + arg_string
        print("cmd_str: " +cmd_str)

        try:
            process = subprocess.Popen(cmd_str)
        except Exception as e:
            raise Exception("error running pdftk: " + str(e))
        return process

    def fill_form_(self, source_fp,
                   context_dict=None,
                   output_fp=None,
                   flatten=False):
        """
        Given a source_file url or path,  a context dict, create an xfdf file and send to pdftk to
           create a merged form
        Args:
            source_fp:
            context_dict:
            output_fp
            flatten:

        Returns:
           output_fp as string
        """

        # check if self.template_file_url is local
        # if it is confirm it exists. if not retrieve and save to local proxy tempfile
        source_fp = test_if_file_is_local_and_if_not_create_proxy(source_fp)
        if not source_fp:
            raise Exception("No local template file for merge")
        # try:
        #     pdftk = mbPDFTK()
        #
        # except:
        #     raise PDFProcessorException("ERROR")
        #
        # fn = pdftk.fill_form(source_filepath=self.source_filepath,
        #                      data_dict_filepath=self.xfdf_filepath,
        #                      flatten=flatten, output_filepath=self.output_filepath)

        xfdf_fp = self.create_xfdf_file(context_dict=context_dict)
        arg_str = self.create_pdftk_arg_string('fill_form',
                                               source_fp,
                                               xfdf_fp,
                                               output_fp)
        if flatten:
            arg_str += " flatten"
        res = ''
        try:
            res = self.run_pdftk_bin(arg_str)
        except Exception as e:
            print("subprocess_result=", res)
            raise PDFProcessorException("Error running pdftk binary:" + str(e))
        else:
            return output_fp

    def extract_bookmarks(self,
                          source_file_url=None,
                          output_fp=None):
        """
        Given a pdf path extract bookmarks to a file
        Args:
            source_file_url:
            output_fp

        """

        pass
