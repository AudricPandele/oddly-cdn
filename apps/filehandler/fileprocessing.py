# -*- coding: utf-8 -*-
import logging; logger = logging.getLogger(__name__)

from django.conf import settings
import sys, os
from pgmagick import Image

from PyPDF2 import PdfFileWriter, PdfFileReader

def main(uploaded_file, mongo_id=None):
    pdfprocessor = PdfProcessor()
    pdfprocessor.run(uploaded_file, mongo_id)

class PdfProcessor(object):
    """
    Simple class to split and flatten pdf to jpeg
    """
    def run(self, uploaded_file, mongo_id):
        inputfile = PdfFileReader(file(str(uploaded_file), "rb"))
        nameinputfile = mongo_id
        self.splitter(inputfile, nameinputfile)
        self.jpeg_converter(nameinputfile)

        
    def splitter(self, inputfile, nameinputfile):
        """
        Actually split the original PDF
        """
        for i in xrange(inputfile.numPages):
            output = PdfFileWriter()
            output.addPage(inputfile.getPage(i))
            outputStream = file("%s%s/%s.pdf" % (settings.MEDIA_ROOT, nameinputfile, i), "wb") # A changer
            output.write(outputStream)
            outputStream.close()
    
    def jpeg_converter(self, nameinputfile):
        """
        Convert splitted pdf pages to flattened JPEG
        """
        p_number = 0
        progressbar = ""
        path = u"%s%s/" % (settings.MEDIA_ROOT, nameinputfile)
        for i in os.listdir(path):
            p_number = p_number + 1
            if i.endswith(".pdf"):
                imgpath = str(settings.MEDIA_ROOT + nameinputfile +"/"+ i)
                img = Image(imgpath)
                #imgname = "%d.jpeg" % (p_number)
                directory = "%s_%s" % (settings.MEDIA_ROOT, nameinputfile) 
                if not os.path.exists(directory):
                    os.mkdir(directory)
                jpegwritepath = str("%s_%s/%s.jpg" % (settings.MEDIA_ROOT, nameinputfile, p_number))
                img.write(jpegwritepath)
            else:
                logger.error("no files")

if __name__ == "__main__":
    main(uploaded_file)
