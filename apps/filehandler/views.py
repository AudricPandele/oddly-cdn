# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response

from django.conf import settings

from pgmagick import Image, Blob
from wand.image import Image as wandimage

QUALITY = {
    'small':'20%',
    'medium':'60%',
    'large':'100%',
    }

def artist_thumb(request, mongoid, quality):
    if request.method == "GET":
        blob = Blob()
        thumb = str("%sartist/thumbs/%s.jpg" % (settings.MEDIA_ROOT, mongoid))
        pgthumb = wandimage(filename=thumb)
        pgthumb.transform(resize = QUALITY.get(quality))
        value = pgthumb.make_blob
        return HttpResponse(value, content_type="image/jpeg")

def artist_cover(request, mongoid, quality):
    if request.method == "GET":
        blob = Blob()
        cover = str("%artist/covers/%s.jpg" % (settings.MEDIA_ROOT, mongoid))
        pgthumb = wandimage(filename=cover)
        pgthumb.transform(resize = QUALITY.get(quality))
        value = pgthumb.make_blob(format='jpeg')
        return HttpResponse(value, content_type="image/jpeg")

def item_file(request, mongoid, quality, page_number):

    if request.method == "GET":
        item = None
        value = None
        if quality == u"SD":
            item_path = "%sitems/pdf/processed/_%s/%s.jpeg" % (settings.MEDIA_ROOT, mongoid, page_number)
            item_file = open(item_path, 'r')
            return HttpResponse(item_file, content_type="image/jpeg")

        if quality == u"HD":
            item_path = "%sitems/pdf/processed/%s/%s.pdf" % (settings.MEDIA_ROOT, mongoid, page_number)
            item_file = open(item_path,'r')
            return HttpResponse(item_file, content_type="application/pdf")

    return HttpResponse(status="400")



def item_cover(request, mongoid, quality):
    if request.method == "GET":
        blob = Blob()
        cover = str("%sitems/covers/%s.jpg" % (settings.MEDIA_ROOT, mongoid))
        pgthumb = wandimage(filename=cover)
        pgthumb.transform(resize = QUALITY.get(quality))
        value = pgthumb.make_blob(format='jpeg')
        return HttpResponse(value, mimetype="image/jpeg")


    
    
