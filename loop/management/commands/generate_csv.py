 # -*- coding: utf-8 -*-
import json
import os
import sys
import MySQLdb
from dg.settings import *
from loop.models import *
import csv
from loop.config import *
from loop.sendmail import *
from django.core.management.base import BaseCommand, CommandError
import xlsxwriter
import time
from datetime import datetime, timedelta
import requests, copy, calendar


class Command(BaseCommand):

    #parse arguments from command line
    def add_arguments(self, parser):
        #create mutually exclusive command line switches
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-fd',
            dest='from_date',
            default=20150701)

        group.add_argument('-nd',
            dest='num_days',
            default=0)

        parser.add_argument('-a',
            dest='aggregator',
            default='all')

        parser.add_argument('-td',
            dest='to_date',
            default=time.strftime('%Y%m%d'))


    
    #generate the excel for the given command line arguments
    def handle(self, *args, **options):
        generate_sheet_for = str(options.get('aggregator'))
        from_date = str(options.get('from_date'))
        to_date = str(options.get('to_date'))
        num_days = int(options.get('num_days'))
        header_json = {}
        data_json = {}
        final_json_to_send = {}
        excel_workbook_name = None

        if num_days < 0: 
            raise CommandError('-nd flag should be > 0')
        elif num_days != 0:
            temp_date = datetime.strptime(to_date, '%Y%m%d')
            from_date = (temp_date - timedelta(days=num_days)).strftime('%Y%m%d')

        #get time period in days and month
        from_day = str(datetime.strptime(from_date, '%Y%m%d').day)
        to_day = str(datetime.strptime(to_date, '%Y%m%d').day)

        from_month = calendar.month_abbr[datetime.strptime(from_date, '%Y%m%d').month]
        to_month = calendar.month_abbr[datetime.strptime(to_date, '%Y%m%d').month]
        if type(generate_sheet_for) != str or type(from_date) != str or len(from_date) != 8 \
            or type(to_date) != str or len(to_date) != 8:
                raise CommandError('Invalid format for arguments')
        elif from_date > to_date:
                raise CommandError('Invalid date range given')
        elif generate_sheet_for != 'all' and generate_sheet_for not in AGGREGATOR_LIST:
                raise CommandError('Aggregator not present in database')            

        query = None
        generate_sheet_for_all_flag = True 
        mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root',
                                           passwd=DATABASES['default']['PASSWORD'],
                                           db=DATABASES['default']['NAME'],
                                            charset = 'utf8',
                                             use_unicode = True)
        
        cur = mysql_cn.cursor()
        #determine the aggregator(s) for whom the sheet is generated
        if generate_sheet_for == 'all' or generate_sheet_for == None:
            query = query_for_all_aggregator % (from_date, to_date, DG_MEMBER_PHONE_LIST, AGGREGATOR_PHONE_LIST)
            excel_workbook_name = 'Incorrect Mobile Numbers_' + from_day + '-' + from_month + ' to ' + \
                                    to_day + '-' + to_month
        else:
            generate_sheet_for_all_flag = False
            query = query_for_single_aggregator % (generate_sheet_for, from_date, to_date, DG_MEMBER_PHONE_LIST, 
                                                    AGGREGATOR_PHONE_LIST)
            excel_workbook_name = 'Incorrect Mobile Numbers_' + generate_sheet_for + '_ ' + from_day + '-' + \
                                    from_month + ' to ' + to_day + '-' + to_month

        cur.execute(query)
        result = cur.fetchall()
        data = [list(row) for row in result]
        #create list copy for filtering
        temp_data = copy.deepcopy(data)
        workbook = xlsxwriter.Workbook(EXCEL_WORKBOOK_NAME)
        header_format = workbook.add_format({'bold':1, 'font_size': 10,'text_wrap': True})
        if generate_sheet_for_all_flag is True:
            #Write data for all aggregators in sheet
            for sno in range(1,len(data) + 1):
                data[sno - 1].insert(0, str(sno))
            sheet_heading = 'Incorrect Mobile Numbers List_'+ from_day + '-' + from_month + ' to ' + to_day + '-' + to_month
            data_json['all'] = {'sheet_heading': sheet_heading,
                                    'sheet_name': 'All Data', 'data': data
                                }
                    
            header_json['all'] = header_dict_for_loop_email_mobile_numbers
            #write data for every aggregator in their respective sheet
            for aggregator_name in AGGREGATOR_LIST:
                #filter data to get rows for the current aggregator
                filtered_data = [row for row in temp_data if row[0] == aggregator_name]
                filtered_data_copy = copy.deepcopy(filtered_data)
                for sno in range(1,len(filtered_data_copy) + 1):
                    filtered_data_copy[sno - 1].insert(0, str(sno))
                sheet_heading = aggregator_name + '_Incorrect Mobile Numbers List_' + \
                from_day + '-' + from_month + ' to ' + to_day + '-' + to_month
                data_json[aggregator_name] = {'sheet_heading': sheet_heading,
                                    'sheet_name': aggregator_name, 'data': filtered_data_copy
                                }
                header_json[aggregator_name] = header_dict_for_loop_email_mobile_numbers
        else:
            #write data for a given aggregator from command line
            for sno in range(1,len(data) + 1):
                data[sno - 1].insert(0, str(sno)) 
            sheet_heading = generate_sheet_for +'_Incorrect Mobile Numbers List_' + \
                                from_day + '-' + from_month + ' to ' + to_day + '-' + to_month 
            data_json[generate_sheet_for] = {'sheet_heading': sheet_heading ,
                                    'sheet_name': generate_sheet_for, 'data': data
                                }
            
            header_json[generate_sheet_for] = header_dict_for_loop_email_mobile_numbers

        final_json_to_send['header'] = header_json
        final_json_to_send['data'] = data_json
        final_json_to_send['cell_format'] = {'bold':0, 'font_size': 10,
                                                    'text_wrap': True}

        #post request to library for excel generation
        r = requests.post('http://localhost:8000/loop/get_payment_sheet/', data=json.dumps(final_json_to_send))
        excel_file = open(excel_workbook_name + '.xlsx', 'w')
        excel_file.write(r.content)
        excel_file.close()
        workbook.close()
        #send email to concerned people with excel file attached    
        common_send_email('Farmers List with Incorrect Mobile Numbers', 
                         RECIPIENTS, excel_file, [],EMAIL_HOST_USER)





