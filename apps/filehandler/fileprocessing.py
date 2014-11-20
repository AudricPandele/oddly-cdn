# -*- coding: utf-8 -*-
import logging; logger = logging.getLogger(__name__)

import sys, os
import requests
import json

from django.conf import settings
from pgmagick import Image

from apps.taskmanager.models import TaskManager

from PyPDF2 import PdfFileWriter, PdfFileReader

def main(task=None, uploaded_file=None, mongo_id=None):
    pdfprocessor = PdfProcessor()
    pdfprocessor.run(uploaded_file, mongo_id)

class PdfProcessor(object):
    """
    Simple class to split and flatten pdf to jpeg
    """
    def run(self, uploaded_file, mongo_id):
        t = self.uploadator(mongo_id)
        self.processed_page = 0
        inputfile = PdfFileReader(file(str(uploaded_file), "rb"))
        self.total_page = inputfile.numPages * 2
        self.splitter(inputfile, mongo_id)
        self.jpeg_converter(mongo_id)

    #-----------------------------------------------------------------------------
    def splitter(self, inputfile, mongo_id):
        """
        Actually split the original PDF
        """

        for i in xrange(inputfile.numPages):
            self.processed_page = self.processed_page + 1
            self.process_update(mongo_id)
            output = PdfFileWriter()
            output.addPage(inputfile.getPage(i))
            outputStream = file("%s%s/%s.pdf" % (settings.MEDIA_ROOT, mongo_id, i), "wb") # A changer
            output.write(outputStream)
            outputStream.close()

    #-----------------------------------------------------------------------------
    def jpeg_converter(self, mongo_id):
        """
        Convert splitted pdf pages to flattened JPEG
        """
        p_number = 0
        progressbar = ""
        path = u"%s%s/" % (settings.MEDIA_ROOT, mongo_id)
        for i in os.listdir(path):
            p_number = p_number + 1
            if i.endswith(".pdf"):
                self.processed_page = self.processed_page + 1
                self.process_update(mongo_id)
                imgpath = str(settings.MEDIA_ROOT + mongo_id +"/"+ i)
                img = Image(imgpath)
                directory = "%s_%s" % (settings.MEDIA_ROOT, mongo_id) 
                if not os.path.exists(directory):
                    os.mkdir(directory)
                jpegwritepath = str("%s_%s/%s.jpg" % (settings.MEDIA_ROOT, mongo_id, p_number))
                img.write(jpegwritepath)
            else:
                logger.error("no files")
                
    #-----------------------------------------------------------------------------
    def process_update(self, mongoid):
        """
        Fetch current process progression to push it to front-end
        """
        current_process_data = round(float(self.processed_page) / float(self.total_page) * 100, 2)
        current_process_entry = TaskManager.objects.filter(book_id = mongoid)
        print current_process_data
        if current_process_entry:
            current_process_entry.update(process_status=current_process_data)
        else:
            TaskManager.objects.create(book_id=mongoid, process_status=0)
            
    #-----------------------------------------------------------------------------
    # def uploadator(self, mongo_id):
    #     """
    #     Upload needed Meta values to API
    #     """
    #     url = 'http://localhost:8000/api/v1/books_meta/'
    #     values = {'book_id' : mongo_id,
    #               'meta_key' : 'test',
    #               'meta_value' : 'test' }
    #     headers = {'content-type': 'application/json', 'referer':'CDN'}
    #     requests.post(url, data=json.dumps(values), headers=headers)
        

if __name__ == "__main__":
    main(uploaded_file)
