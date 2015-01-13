# Python shit
import os

# Django shit
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Image shit
from pgmagick import Image


def uploadImage(file = None, relativePath = "", absolutePath = "", extensionPath = ""):
    if file:
        default_storage.save(relativePath, ContentFile(file.read()))
        convertImage(oldPath = absolutePath, newPath = extensionPath)


def convertImage(oldPath, newPath):
    _img = Image(oldPath)
    _img.write(newPath)
    os.remove(oldPath)
