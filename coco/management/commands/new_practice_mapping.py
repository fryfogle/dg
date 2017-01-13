# python imports
# django imports
from django.core.management.base import BaseCommand
# project imports
from coco.new_practice_map import PracticeMapping


class Command(BaseCommand):
    help = 'Prepare the data for export'

    def handle(self, *args, **options):
        hnn_obj = PracticeMapping()
        hnn_obj.run()