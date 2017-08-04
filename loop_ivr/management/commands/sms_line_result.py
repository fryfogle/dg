__author__ = 'Vikas Saini'

import MySQLdb
import itertools
import pandas as pd

from dg.settings import DATABASES

from django.core.management.base import BaseCommand
from django.db.models import get_model

from loop.models import Crop, Mandi, CropLanguage
from loop_ivr.models import PriceInfoIncoming

from loop_ivr.utils.config import AGGREGATOR_SMS_NO, mandi_hi, indian_rupee, \
    agg_sms_initial_line, agg_sms_no_price_for_combination, agg_sms_no_price_available

from loop_ivr.utils.marketinfo import raw_sql

from datetime import datetime, timedelta

class Command(BaseCommand):

    crop_map = dict()
    mandi_map = dict()
    crop_in_hindi_map = dict()
    all_crop = Crop.objects.values('id', 'crop_name')
    all_mandi = Mandi.objects.values('id', 'mandi_name')
    crop_in_hindi = CropLanguage.objects.filter(language_id=1).values('crop_id', 'crop_name')
    for crop in all_crop:
       crop_map[crop['id']] = crop['crop_name']
    for mandi in all_mandi:
       mandi_map[mandi['id']] = mandi['mandi_name']
    for crop in crop_in_hindi:
        crop_in_hindi_map[crop['crop_id']] = crop['crop_name']

    def run_query(self,query):
        mysql_cn = MySQLdb.connect(host=DATABASES['default']['HOST'], port=DATABASES['default']['PORT'], 
            user=DATABASES['default']['USER'] ,
            passwd=DATABASES['default']['PASSWORD'],
            db=DATABASES['default']['NAME'],
            charset = 'utf8',
            use_unicode = True)
        cursor = mysql_cn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows


    def get_price_info(self, crop_list, mandi_list, requested_date, all_crop_flag, all_mandi_flag):
        price_info_list = []
        price_info_list.append(agg_sms_initial_line)
        today_date = datetime.now()
        raw_query = raw_sql.last_three_trans.format('(%s)'%(crop_list[0],) if len(crop_list) == 1 else crop_list, '(%s)'%(mandi_list[0],) if len(mandi_list) == 1 else mandi_list, tuple((requested_date-timedelta(days=day)).strftime('%Y-%m-%d') for day in range(0,3)))
        query_result = self.run_query(raw_query)
        if not query_result:
            price_info_list.append(agg_sms_no_price_available)
        else:
            crop_mandi_comb = []
            prev_crop, prev_mandi, crop_name, mandi_name = -1, -1, '', ''
            for row in query_result:
                crop, mandi, date, min_price, max_price, mean = row['crop'], row['mandi'], row['date'], int(row['minp']), int(row['maxp']), int(row['mean'])
                if crop != prev_crop or mandi != prev_mandi:
                    if not all_crop_flag and not all_mandi_flag:
                        crop_mandi_comb.append((crop,mandi))
                    prev_crop, prev_mandi = crop, mandi
                    crop_name = self.crop_in_hindi_map.get(crop).encode("utf-8") if self.crop_in_hindi_map.get(crop) else self.crop_map[crop].encode("utf-8")
                    mandi_name = self.mandi_map[mandi].encode("utf-8")
                    temp_str = ('\n%s,%s %s\n')%(crop_name,mandi_name.rstrip(mandi_hi).rstrip(),mandi_hi)
                    price_info_list.append(temp_str)
                if max_price-min_price >= 2:
                    min_price = mean-1
                    max_price = mean+1
                if min_price != max_price:
                    temp_str = ('%s: %s %s-%s\n')%(date.strftime('%d-%m-%Y'),indian_rupee,str(min_price),str(max_price))
                else:
                    temp_str = ('%s: %s %s\n')%(date.strftime('%d-%m-%Y'),indian_rupee,str(max_price))
                price_info_list.append(temp_str)
            if not all_crop_flag and not all_mandi_flag:
                for crop, mandi in itertools.product(crop_list, mandi_list):
                    if (crop,mandi) not in crop_mandi_comb:
                        crop_name = self.crop_in_hindi_map.get(crop).encode("utf-8") if self.crop_in_hindi_map.get(crop) else self.crop_map[crop].encode("utf-8")
                        mandi_name = self.mandi_map[mandi].encode("utf-8")
                        temp_str = ('\n%s,%s %s\n')%(crop_name,mandi_name.rstrip(mandi_hi).rstrip(),mandi_hi)
                        price_info_list.append(temp_str)
                        price_info_list.append(agg_sms_no_price_for_combination)
        final_result = ''.join(price_info_list)        
        return final_result


    def get_valid_list(self,app_name, model_name, requested_item):
        model = get_model(app_name, model_name)
        id_list = set(model.objects.values_list('id', flat=True))
        requested_list = set(int(item) for item in requested_item.split('*') if item)
        if (0 in requested_list):
            return tuple(map(int,id_list)),1
        return tuple(map(int,requested_list.intersection(id_list))),0

    def write_data(self,data):
        data_df = pd.DataFrame(data)
        writer = pd.ExcelWriter('sms_info_price.xlsx', engine='xlsxwriter')
        data_df.to_excel(writer, sheet_name='sms_info')
        writer.save()

    def handle(self, *args, **options):
        price_info_obj_list = list(PriceInfoIncoming.objects.filter(info_status__in=[0,1]).values('id','from_number','incoming_time',
                                'info_status','query_code','price_result'))
        for price_info_dict in price_info_obj_list:
            query_code = price_info_dict['query_code'].split('**')
            if len(query_code) != 2:
                continue
            crop_info, mandi_info = query_code[0], query_code[1]
            crop_list, all_crop_flag = self.get_valid_list('loop', 'crop', crop_info)
            mandi_list, all_mandi_flag = self.get_valid_list('loop', 'mandi', mandi_info)
            if (all_crop_flag and all_mandi_flag) or (not crop_list) or (not mandi_list):
                continue
            requested_date = price_info_dict['incoming_time']
            current_price_result = self.get_price_info(crop_list, mandi_list, requested_date, all_crop_flag, all_mandi_flag)
            price_info_dict['current_price_result'] = current_price_result
        self.write_data(price_info_obj_list)