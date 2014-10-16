from django.contrib import admin

from apps.filehandler.models import FileHandler
from apps.filehandler import fileprocessing

class FileHandlerAdmin(admin.ModelAdmin):
    
    class Meta:
        pass
    
    def save_model(self, request, obj, form, change):
        obj.save()
        current_file_path =  request.request.FILES.get('file')
        fileprocessing.main(current_file_path)
        
admin.site.register(FileHandler, FileHandlerAdmin)

