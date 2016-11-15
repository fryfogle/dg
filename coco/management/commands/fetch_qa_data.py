# python imports
# django imports
from django.core.management.base import BaseCommand
# project imports
from coco.qa_export import QAData


class Command(BaseCommand):
    help = 'Prepare the data for export'

    def handle(self, *args, **options):
        hnn_obj = QAData()
        hnn_obj.run()