# -*- coding: utf-8 -*-
import logging; logger = logging.getLogger(__name__)

from django.conf import settings
import sys, os
from pgmagick import Image

from PyPDF2 import PdfFileWriter, PdfFileReader

def main(uploaded_file, mongo_id=None):
    pdfprocessor = PdfProcessor()
    pdfprocessor.run(uploaded_file)

class PdfProcessor(object):
    

    def run(self, uploaded_file):
        inputfile = PdfFileReader(file(str(uploaded_file), "rb"))
        nameinputfile = "none"
        self.splitter(inputfile, nameinputfile)
        self.jpeg_converter(nameinputfile)
        
    def splitter(self, inputfile, nameinputfile):
         for i in xrange(inputfile.numPages):
             output = PdfFileWriter()
             output.addPage(inputfile.getPage(i))
             outputStream = file("%s_%s.pdf" % (nameinputfile, i), "wb") # A changer
             output.write(outputStream)
             outputStream.close()
    
    def jpeg_converter(self, nameinputfile):
        p_number = 0
        progressbar = ""
        for i in os.listdir(settings.MEDIA_ROOT):
            p_number = p_number + 1
            if i.endswith(".pdf"):
                imgpath = settings.MEDIA_ROOT + i
                img = Image(imgpath)
                imgname = "%s_%d.jpeg" % (os.path.splitext(i)[0], p_number)
                img.write(settings.MEDIA_ROOT + imgname)
            else:
                print("no files")

if __name__ == "__main__":
    main(uploaded_file)
