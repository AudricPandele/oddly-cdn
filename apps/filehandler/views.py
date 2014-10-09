from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from apps.filehandler.forms import FileHandlerForm
from fileprocessing import main as FileProcessingFunction

def upload_file(request):
    if request.method == 'POST':
        form = (request.POST, request.FILES)
        if form.is_valid():
            FileProcessingFunction(request.FILES['uploaded_file'])
            return HttpResponseRedirect('/')
    else:
        form = FileHandlerForm()
    return HttpResponseRedirect('/')
