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

def check_value(val):
    if val is not None and isinstance(val, unicode):
        return val.encode('ascii', 'ignore').decode('ascii')
    else:
        return val


def break_word_value_and_identify_category(value):
    # we will have a list of related practice
    # we need to pick each word and find the same word in category , subcategory or video practice
    data_list = []
    if value is not None and isinstance(value, unicode):
        val = value.encode('ascii', 'ignore').decode('ascii')
        # this means we have valid string in val
        # now split the string
        # now begins val from table
        if val.find(",") and len(val.split(",")) > 0:
            for idx, var in enumerate([str(item).strip(' ') for item in val.split(',')]):
                if var is not None and var != '':
                    # first from the category.
                    category_list = Category.objects.filter(category_name__icontains=var, category_name__isnull=False).values('category_name')
                    if len(category_list):
                        data_list.append(category_list[0].get('category_name'))
                    # then check subcategory
                    if not category_list:
                        sub_category_list = SubCategory.objects.filter(subcategory_name__icontains=var, subcategory_name__isnull=False).values('subcategory_name')
                        if len(sub_category_list):
                            data_list.append(sub_category_list[0].get('subcategory_name'))
                    if not category_list:
                        videopractice = VideoPractice.objects.filter(videopractice_name__icontains=var, videopractice_name__isnull=True).values('videopractice_name')
                        if len(videopractice):
                            data_list.append(videopractice[0].get('videopractice_name'))


    
    return data_list


def break_word_value_and_identify_subcategory(value):
    # we will have a list of related practice
    # we need to pick each word and find the same word in category , subcategory or video practice
    data_list = []
    if value is not None and isinstance(value, unicode):
        val = value.encode('ascii', 'ignore').decode('ascii')
        # this means we have valid string in val
        # now split the string
        # now begins val from table
        if val.find(",") and len(val.split(",")) > 0:
            for idx, var in enumerate([str(item).strip(' ') for item in val.split(',')][1:]):
                if var is not None and var != '':
                    var = var.lower()
                    print "VAR:", var
                    sub_category_list = SubCategory.objects.filter(subcategory_name__icontains=var, subcategory_name__isnull=False).values('subcategory_name')
                    if len(sub_category_list):
                        data_list.append(sub_category_list[0].get('subcategory_name'))
                    if not sub_category_list:
                        videopractice = VideoPractice.objects.filter(videopractice_name__icontains=var, videopractice_name__isnull=True).values('videopractice_name')
                        if len(videopractice):
                            data_list.append(videopractice[0].get('videopractice_name'))
    print "Subcategory_from_function:   ", data_list
    return data_list


def calculate_category(rp, existing_value, list_value):
    category_val = None
    if existing_value is not None:
        category_val = existing_value.encode('ascii', 'ignore').decode('ascii')
        return category_val
    if existing_value is None and rp is not None:
        category_val = list_value[0] if len(list_value) else category_val
    # print "Category>>>", category_val, "RP>>>>", rp, "Existing>>>>", existing_value,"LIST>>>>", list_value
    return category_val

def calculate_subcategory(rp, existing_value, list_value):
    subcategory_val = None
    if existing_value is not None:
        subcategory_val = existing_value.encode('ascii', 'ignore').decode('ascii')
        return subcategory_val
    if existing_value is None and rp is not None:
        subcategory_value = list_value[0] if len(list_value) else subcategory_val
    print "SubCategory>>>", subcategory_val, "RP>>>>", rp, "Existing>>>>", existing_value,"LIST>>>>", list_value
    return subcategory_val


class PracticeMapping(object):
    """
    Prepare the data for export
    """

    def run(export):
        from datetime import datetime
        rp_list_value = []
        rp_list_value_for_subcategory = []
        export = True
        filename = settings.PROJECT_PATH +'/practice-map-data-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
        data_list = []
        if export:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = \
                'attachment; filename=%s' % filename
            outfile = open(filename, 'wb')
            writer = csv.writer(outfile)
            writer.writerow([
                             # 'State',
                             'District',
                             'Video ID',
                             'Video Name',
                             '',
                             'Related Practices',
                             '',
                             'Category',
                             'Sub Category',
                             'Practice',
                             # 'YouTubeID'
                             ])

            vid_obj = Video.objects.filter(village__block__district__state__country_id=1,
                                           village__block__district__state_id=21).values('id', 'title',
                                           'village__block__district__district_name',
                                           'village__block__district__state__state_name',
                                           'village__block__district__state_id',
                                           'village__block__district_id',
                                           'category__category_name', 'subcategory__subcategory_name',
                                           'videopractice_id',
                                           'related_practice_id',
                                           'related_practice__practice_name',
                                           'videopractice__videopractice_name',
                                           # 'youtubeid',
                                           ).order_by('-id')
            for idx, iterable in enumerate(vid_obj):
                rp = iterable.get('related_practice__practice_name')
                if rp is not None:
                    # begin manipulation from here
                    rp_list_value = break_word_value_and_identify_category(rp)
                    rp_list_value_for_subcategory = \
                        break_word_value_and_identify_subcategory(rp)
                try:
                    writer.writerow([
                                    # check_value(iterable.get('village__block__district__state__state_name')),
                                    check_value(iterable.get('village__block__district__district_name')),
                                    iterable.get('id'),
                                    check_value(iterable.get('title')),
                                    '',
                                    check_value(iterable.get('related_practice__practice_name')),
                                    '',
                                    calculate_category(rp, iterable.get('category__category_name'), rp_list_value),
                                    calculate_subcategory(rp, iterable.get('category__subcategory_name'), rp_list_value_for_subcategory),
                                    #check_value(iterable.get('subcategory__subcategory_name')),
                                    check_value(iterable.get('videopractice__videopractice_name')),
                                    # iterable.get('youtubeid')
                                    ])
                except Exception as e:
                    print e

            return response
