# -*- coding: utf-8 -*-
import logging; logger = logging.getLogger(__name__)

import sys, os
from pgmagick import Image

from PyPDF2 import PdfFileWriter, PdfFileReader

def main(uploaded_file, mongo_id=None):
    pdfprocessor = PdfProcessor()
    pdfprocessor.run()

class PdfProcessor(object):
    
    INPUTFILE = PdfFileReader(file("doc.pdf", "rb"))

    def run(self):
        pdf = self.INPUTFILE
        documents_infos = self.retrieve_document_infos(pdf)
        self.splitter(documents_infos)
        self.jpeg_converter()
        
    def splitter(self, documents_infos):
         for i in xrange(self.INPUTFILE.numPages):
             output = PdfFileWriter()
             output.addPage(self.INPUTFILE.getPage(i))
             outputStream = file("%s.pdf" % i, "wb") # A changer
             output.write(outputStream)
             outputStream.close()
  
    def jpeg_converter(self):
        p_number = 0
        progressbar = ""

        for i in os.listdir(os.getcwd()):
            p_number = p_number + 1
            if i.endswith(".pdf"):
                img = Image(i)
                img.write("page_%d.jpeg" % p_number)
            else:
                print("no files")

if __name__ == "__main__":
    main(uploaded_file)
