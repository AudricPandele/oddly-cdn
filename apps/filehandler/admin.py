from django.contrib import admin

from apps.filehandler.models import FileHandler
from apps.filehandler import fileprocessing

class FileHandlerAdmin(admin.ModelAdmin):
    
    class Meta:
        pass
    
    def save_model(self, request, obj, form, change):
        import pdb; pdb.set_trace()

admin.site.register(FileHandler, FileHandlerAdmin)

