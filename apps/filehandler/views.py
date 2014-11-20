from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from apps.filehandler.forms import FileHandlerForm
from fileprocessing import main as FileProcessingFunction

from django.conf import settings

from pgmagick import Image, Blob

def upload_file(request):
    if request.method == 'POST':
        form = (request.POST, request.FILES)
        if form.is_valid():
            FileProcessingFunction(request.FILES['uploaded_file'])
            return HttpResponseRedirect('/')
    else:
        form = FileHandlerForm()
    return HttpResponseRedirect('/')

def get_thumb(request):
    if request.method == "GET":

        blob = Blob()
        mongoid = request.path.split('/')
        thumb = str("%sthumbs/%s.jpg" % (settings.MEDIA_ROOT, mongoid[2]))
        pgthumb = Image(thumb)
        pgthumb.scale('100x100')
        pgthumb.write(blob)
        value = blob.data        

        return HttpResponse(value, content_type="image/jpeg")
