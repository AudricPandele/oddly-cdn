# -*- coding: utf-8 -*-
import logging; logger = logging.getLogger(__name__)

import sys, os
import requests
import json

from django.conf import settings

from pgmagick import Image, FilterTypes
from PyPDF2 import PdfFileWriter, PdfFileReader

from wand.image import Image as wandimage

from apps.taskmanager.models import TaskManager


#-----------------------------------------------------------------------------
def main(task=None, uploaded_file=None, mongo_id=None):
    pdfprocessor = PdfProcessor()
    pdfprocessor.run(uploaded_file, mongo_id)



#-----------------------------------------------------------------------------
class PdfProcessor(object):
    """
    Simple class to split and flatten pdf to jpeg
    """
    def run(self, uploaded_file, mongo_id):
        # Processed_page = total de pages  traitée pour génerer un statut de progression
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
        # Je crée mon dossier si il n'existe pas
        directory = "%sitems/pdf/processed/%s" % (settings.MEDIA_ROOT, mongo_id)
        if not os.path.exists(directory):
            os.mkdir(directory)
            
        for i in xrange(inputfile.numPages):
            # Je considère que le nombre de pages converties s'incrémente de 1
            # Je met à jour le process status   pour l'afficher dans le front
            self.processed_page = self.processed_page + 1
            self.process_update(mongo_id)
            
            output = PdfFileWriter()
            output.addPage(inputfile.getPage(i))
            outputStream = file("%sitems/pdf/processed/%s/%s.pdf" % (settings.MEDIA_ROOT, mongo_id, i), "wb")
            output.write(outputStream)
            outputStream.close()

    #-----------------------------------------------------------------------------
    def jpeg_converter(self, mongo_id):
        """
        Convert splitted pdf pages to flattened JPEG
        """
        # Le numéro est initialisé à -1 sinon il prend la page 1 et pas la page 0
        p_number = -1
        progressbar = ""
        path = u"%sitems/pdf/processed/%s" % (settings.MEDIA_ROOT, mongo_id)
        for i in os.listdir(path):
            
            # Je récupère chaque page du livre uploadé
        
            p_number = p_number + 1
            if i.endswith(".pdf"):
                i = "%s.pdf" % p_number
                
                # Je considère que le nombre de pages converties s'incrémente de 1
                # Je met à jour le process status   pour l'afficher dans le front
                self.processed_page = self.processed_page + 1
                self.process_update(mongo_id)

                print "This is the file %s" % (i)
                print "This is the page number %d" % (p_number)
                # Je récupère le chemin absolu de mon pdf
                # Je crée mon fichier image
                # J'indique l'emplacement de sauvegarde du jpeg
                imgpath = str(settings.MEDIA_ROOT + "items/pdf/processed/" + mongo_id +"/"+ i)
                
                img = wandimage(filename=imgpath, resolution=200)
                directory = "%sitems/pdf/processed/_%s" % (settings.MEDIA_ROOT, mongo_id)

                # Je crée mon dossier si il n'existe pas
                if not os.path.exists(directory):
                    os.mkdir(directory)

                # J'écris mon jpeg
                jpegwritepath = str("%sitems/pdf/processed/_%s/%s.jpeg" % (settings.MEDIA_ROOT, mongo_id, p_number))
                img.ALPHA_CHANNEL_TYPES = ('flatten',)
                img.format = 'jpeg'
                img.compression_quality = 70
                print jpegwritepath
                img.save(filename=jpegwritepath)
                
            else:
                logger.error("no files")
                
    #-----------------------------------------------------------------------------
    def process_update(self, mongoid):
        """
        Fetch current process progression to push it to front-end
        """
        # MUCH MATH SO SCIENCE
        current_process_data = round(float(self.processed_page) / float(self.total_page) * 100, 2)
        current_process_entry = TaskManager.objects.filter(book_id = mongoid)
        logger.info(current_process_data)
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
