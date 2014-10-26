from __future__ import absolute_import

from celery import shared_task

from apps.filehandler import fileprocessing

@shared_task
def run_parser(uploaded_file=None, mongo_id=None):
    fileprocessing.main(uploaded_file=uploaded_file, mongo_id=mongo_id)

