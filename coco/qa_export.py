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
from qacoco.models import *


class QAData(object):
    """
    Prepare the data for export
    """

    def run(export):
        from datetime import datetime
        export = True
        filename = settings.PROJECT_PATH +'/qa-data-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
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
                             'Video Quality Review',
                             'Dissemination Quality',
                             'Adoption Verification',
                             ])
            data_list = VideoQualityReview.objects.filter(video__village__block__district__state__country_id=1
                                            ).values_list('video__village__block__district__state__country_id',
                                                          'video__village__block__district__state_id',
                                                          'video__village__block__district__state__country__country_name',
                                                          'video__village__block__district__state__state_name'
                                                          ).distinct()

            for idx, iterable in enumerate(data_list):
                
                
                vqr_obj = \
                    VideoQualityReview.objects.filter(video__village__block__district__state__country_id=iterable[0],
                                                      video__village__block__district__state_id=iterable[1],
                                                      time_created__range=["2016-07-18", "2016-10-31"],
                                                      )
                
                dsq_obj = \
                    DisseminationQuality.objects.filter(village__block__district__state__country_id=iterable[0],
                                                        village__block__district__state_id=iterable[1],
                                                        time_created__range=["2016-07-18", "2016-10-31"],
                                                        )

                adp_obj = \
                    AdoptionVerification.objects.filter(village__block__district__state__country_id=iterable[0],
                                                        village__block__district__state_id=iterable[1],
                                                        time_created__range=["2016-07-18", "2016-10-31"],
                                                        )

                
                try:
                    writer.writerow([
                                    iterable[2],
                                    iterable[3],
                                    vqr_obj.count() if len(vqr_obj) else 0,
                                    dsq_obj.count() if len(dsq_obj) else 0,
                                    ])
                except Exception as e:
                    print e

            return response