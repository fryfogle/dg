# python imports
# django imports
from django.core.management.base import BaseCommand
# project imports
from coco.export_data import VideoData


class Command(BaseCommand):
    help = 'Prepare the data for export'

    def handle(self, *args, **options):
        hnn_obj = VideoData()
        hnn_obj.run()