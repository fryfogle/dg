import time
import datetime
from datetime import timedelta
from pytz import timezone

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dg.settings import EXOTEL_ID, EXOTEL_TOKEN, EXOTEL_HELPLINE_NUMBER, MEDIA_ROOT

from loop.models import HelplineExpert, HelplineIncoming, HelplineOutgoing, PhoneVerificationIVR
from loop.helpline_view import get_status, write_log

HELPLINE_LOG_FILE = '%s/loop/helpline_log.log'%(MEDIA_ROOT,)

class Command(BaseCommand):

    def handle(self, *args, **options):

        verification_objs = PhoneVerificationIVR.objects.filter(call_duration=None)
        for obj in verification_objs:
            call_id = str(obj.call_id)
            call_status = get_status(call_id)
            call_duration = str(datetime.datetime.strptime(call_status['end_time'],'%Y-%m-%d %H:%M:%S') \
                             - datetime.datetime.strptime(call_status['start_time'],'%Y-%m-%d %H:%M:%S'))
            try:
                obj.call_duration = call_duration
                obj.save()
            except Exception as e:
                print str(e)
                module = "response_duration_assignment"
                write_log(HELPLINE_LOG_FILE,module,str(e))
            time.sleep(1)





