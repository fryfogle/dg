# python imports
import csv
# django imports
from django.http import HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.db.models import *
from django.db.models import Q
#app imports 
from videos.models import *
from geographies.models import *
from videos.models import *


class VideoData(object):
    """
    Prepare the data for export
    """

    def run(export):
        from datetime import datetime
        export = True
        filename = settings.PROJECT_PATH +'/video-data-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
        data_list = []
        screening_days_delay_list = []
        #for csv
        abg_adop = None
        if export:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = \
                'attachment; filename=%s' % filename
            outfile = open(filename, 'wb')
            writer = csv.writer(outfile)
            writer.writerow(['Country',
                             'State',
                             'Videos Entered in System',
                             'Practise Mapped',
                             'Non-Negotiable',
                             ])
            data_list = Video.objects.filter(village__block__district__state__country_id=1
                                            ).values_list('village__block__district__state__country_id',
                                                          'village__block__district__state_id',
                                                          'village__block__district__state__country__country_name',
                                                          'village__block__district__state__state_name'
                                                          ).distinct()

            for idx, iterable in enumerate(data_list):
                
                # videos produced
                vid_obj = Video.objects.filter(village__block__district__state__country_id=iterable[0],
                                               village__block__district__state_id=iterable[1],
                                               time_created__range=["2016-07-18", "2016-10-31"],
                                               )
                #practise mapped
                non = 0
                video_practise = 0
                if len(vid_obj):
                    # import pdb
                    # pdb.set_trace()
                    video_practise = vid_obj.filter(videopractice__isnull=False).count()
                    vid_id_list = [d['id'] for d in vid_obj.values('id') if 'id' in d]
                    non_nego = NonNegotiable.objects.filter(id__in=vid_id_list)
                    non = len(non_nego)
                try:
                    writer.writerow([
                                    iterable[2],
                                    iterable[3],
                                    vid_obj.count(),
                                    video_practise,
                                    non
                                    ])
                except Exception as e:
                    print e

            return response