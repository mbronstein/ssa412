# pdftemplate.py

import os
import time
from PyPDF2 import PdfFileReader, PdfFileWriter
from docxtpl import DocxTemplate
from flask import make_response
from tempfile import TemporaryFile
from io import BytesIO
from reportlab.pdfgen import canvas




class FileNotFound(Exception):
    pass

class UnknownFileExtension(Exception):
    pass

class MergeFormError(Exception):
    pass

class MergeTemplate(object):
    def __init__(self, formfname, form_dirpath, output_dirpath=None):
        self.formfname = formfname
        self.form_fpath = os.path.join(form_dirpath, formfname)
        if not os.path.exists(self.form_fpath):
            raise FileNotFound

        with open(self.form_fpath, 'rb') as f:
            self.template_buff = BytesIO(f.read())

        self.formfname_ext = os.path.splitext(formfname)[1][1:]
        self.output_dirpath = output_dirpath
        self.output_filepath = None

    def create_output_fn(self, client=None):
        if not client:
            client = "xxx"
        else:
            client = client[0:8]
        retval = "{0}_{1}_{2}.{3}".format(client,
                                          os.path.splitext(self.formfname)[0][0:10],
                                          time.strftime("%H-%M-%S", time.localtime()),
                                          self.formfname_ext)
        return retval

    def context_to_pdf_field_datadict(self, xcontext):
        """assuming context is a dictionarie of objects, combine in an new dictoanry
        containing ...
        """
        retdict = {}
        for key, obj in xcontext.items():  # for each string key including 'contact', 'fo', .... assign to data_obj

            for k, v in obj.mergefield_dict().items():  # for each field  in each data object create field entry with field name and prefix
                retdict["{0}_{1}".format(key, k)] = v
        return retdict

    def render(self, context):
        self.mergedata_dict = self.context_to_pdf_field_datadict(context)
        contact_name = self.mergedata_dict.get('contact_last_name', 'xxx')
        self.output_filename = self.create_output_fn(contact_name)
        self.output_filepath = os.path.join(self.output_dirpath, self.output_filename)
        self.template = None
        if self.formfname_ext.upper() == 'PDF':
            s = self.merge_pdf_and_save()
            # bstream = self.merge_pdf_with_data()
        elif self.formfname_ext.upper() in ('DOCX', 'DOC'):
            bstream = self.merge_docx_with_data()
        else:
            return "Error"
        # with open(self.output_filepath, 'wb') as f:
        #     f.write(bstream.getvalue())
        #     f.close()
        # return self.output_filepath

    def merge_pdf_with_data(self):
        pdfreader = PdfFileReader(open(self.form_fpath, 'rb'))
        self.pdf_field_dict = pdfreader.getFields()
        pdfwriter = PdfFileWriter()

        for pageNum in range(pdfreader.getNumPages()):
            pageobj = pdfreader.getPageNumber(pageNum)
            pdfwriter.addPage(pageobj)

        for pageNum in range(pdfwriter.getNumPages()):
            pageObj = pdfreader.getPage(pageNum)
            pdfwriter.updatePageFormFieldValues(pageObj, self.mergedata_dict)
        # bstream = BytesIO()
        # self.output_buff = bstream
        # pdfwriter.write(bstream)
        # bstream.seek(0)
        # return bstream
        with open(self.output_filepath, 'wb') as f:
            pdfwriter.write(f)



    def merge_pdf_and_save(self):
        pdfreader = PdfFileReader(open(self.form_fpath, 'rb'))
        self.pdf_field_dict = pdfreader.getFields()
        pdfwriter = PdfFileWriter()
        for page in range(pdfreader.getNumPages()):
            pdfwriter.addPage(pdfreader.getPage(page))
        for pageNum in range(pdfwriter.getNumPages()):
             pageObj = pdfreader.getPage(pageNum)
             pdfwriter.updatePageFormFieldValues(pageObj, self.mergedata_dict)
        with open(self.output_filepath, 'wb') as f:
            pdfwriter.write(f)
            f.close()
        return self.output_filepath

    def copy_pdf_and_save(self):
        self.output_filename = self.create_output_fn('xxx')
        pdfreader = PdfFileReader(open(self.form_fpath, 'rb'))
        self.output_filepath = os.path.join(self.output_dirpath, self.output_filename)
        pdfwriter = PdfFileWriter()
        pdfwriter.cloneReaderDocumentRoot(pdfreader)
        for page in range(pdfreader.getNumPages()):
             pdfwriter.addPage(pdfreader.getPage(page))
        with open(self.output_filepath, 'wb') as f:
            pdfwriter.write(f)
            f.close()
        return self.output_filepath

    def merge_docx_with_data(self):
        try:
            form = DocxTemplate(self.form_fpath)
            form.render(self.mergedata_dict)
            bstream = BytesIO()
            self.output_buff = bstream
            form.save(bstream)
            bstream.seek(0)
            return bstream
        except:
            raise MergeFormError

    def create_pdf_with_image(imgPath):

        # Using ReportLab to insert image into PDF
        imgTemp = BytesIO()
        imgDoc = canvas.Canvas(imgTemp)
        # Draw image on Canvas and save PDF in buffer
        imgDoc.drawImage(imgPath, 0,0,1700,2200)  ## at (399,760) with size 160x160
        imgDoc.save()

        # Use PyPDF to merge the image-PDF into the template
        page = PdfFileReader(file("imagedocument.pdf", "rb")).getPage(0)
        overlay = PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0)
        page.mergePage(overlay)

        # Save the result
        output = PdfFileWriter()
        output.addPage(page)
        output.write(file("output.pdf", "w"))
        output.close()

        # Create the watermark from an image
        c = canvas.Canvas('form_image.pdf')

        # Draw the image at x, y. I positioned the x,y to be where i like here
        c.drawImage(imgPath, 1700, 2200)

        # Add some custom text for good measure
        c.drawString(15, 720, "Hello World")
        c.save()

        # Get the watermark file you just created
        watermark = PdfFileReader(open("watermark.pdf", "rb"))

        # Get our files ready
        output_file = PdfFileWriter()
        input_file = PdfFileReader(open("test2.pdf", "rb"))

        # Number of pages in input document
        page_count = input_file.getNumPages()

        # Go through all the input file pages to add a watermark to them
        for page_number in range(page_count):
            print "Watermarking page {} of {}".format(page_number, page_count)
            # merge the watermark with the page
            input_page = input_file.getPage(page_number)
            input_page.mergePage(watermark.getPage(0))
            # add page from input file to output document
            output_file.addPage(input_page)

        # finally, write "output" to document-output.pdf
        with open("document-output.pdf", "wb") as outputStream:
            output_file.write(outputStream)

if __name__ == '__main__':
    pass