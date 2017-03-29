import json

import datetime
from django.contrib.auth.models import User
from django.db.models import get_model
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from tastypie.models import ApiKey


class TimestampException(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class DatetimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def save_log(sender, **kwargs):
    LoopUser = get_model('loop', 'LoopUser')
    instance = kwargs["instance"]
    sender = sender.__name__  # get the name of the table which sent the request
    try:
        action = kwargs["created"]
    except Exception:
        action = -1
    try:
        # user = User.objects.get(id=instance.user_modified_id) if instance.user_modified_id else User.objects.get(
            # id=instance.user_created_id)
        user = instance.user_created
    except Exception, ex:
        user = None

    model_id = instance.id
    loop_user = None
    village_id = None

    if sender == "Village":
        village_id = instance.id
    elif sender == "CombinedTransaction":
        village_id = instance.farmer.village.id
        loop_user = LoopUser.objects.get(user=instance.user_created)
    elif sender == "Transporter":
        if instance.user_created is not None:
            loop_user = LoopUser.objects.get(user=instance.user_created)
        else:
            loop_user = None
    elif sender == "TransportationVehicle":
        if instance.user_created is not None:
            loop_user = LoopUser.objects.get(user=instance.user_created)
        else:
            loop_user = None
    elif sender == "DayTransportation":
        loop_user = LoopUser.objects.get(user=instance.user_created)
    elif sender == "LoopUserAssignedMandi":
        sender = "Mandi"
        model_id = instance.mandi.id
        loop_user = instance.loop_user
    elif sender == "LoopUserAssignedVillage":
        sender = "Village"
        model_id = instance.village.id
        village_id = instance.village.id
        loop_user = instance.loop_user
        sender = "Village"
    elif sender == "Farmer":
        village_id = instance.village.id

    Log = get_model('loop', 'Log')
    log = Log(village=village_id, user=user, action=action, entry_table=sender,
              model_id=model_id, loop_user=loop_user)
    log.save()

    if action == -1:
        LogDeleted = get_model('loop','LogDeleted')
        obj = model_to_dict(instance)
        deletedObject = LogDeleted(entry_table=sender,table_object=obj)
        deletedObject.save()


def get_log_object(log_object):
    Obj_model = get_model('loop', log_object.entry_table)
    try:
        obj = Obj_model.objects.get(id=log_object.model_id)
        data = {'log': model_to_dict(log_object, exclude=['loop_user', 'user', 'village', 'id']), 'data': model_to_dict(
            obj), 'online_id': obj.id}
    except Exception, e:
        data = {'log': model_to_dict(
            log_object, exclude=['loop_user', 'user', 'village', 'id']), 'data': None, 'online_id': log_object.model_id}
    return data


def get_latest_timestamp():
    Log = get_model('loop', 'Log')
    try:
        timestamp = Log.objects.latest('id')
    except Exception as e:
        timestamp = None
    return timestamp


@csrf_exempt
def send_updated_log(request):
    if request.method == 'POST':
        apikey = request.POST['ApiKey']
        timestamp = request.POST['timestamp']
        if timestamp:
            try:
                apikey_object = ApiKey.objects.get(key=apikey)
                user = apikey_object.user
            except Exception, e:
                return HttpResponse("-1", status=401)
            LoopUser = get_model('loop', 'LoopUser')
            try:
                requesting_loop_user = LoopUser.objects.get(user_id=user.id)
                user_list = LoopUser.objects.filter(
                    village__block_id=requesting_loop_user.village.block.id).values_list('user__id', flat=True)
            except Exception as e:
                raise UserDoesNotExist(
                    'User with id: ' + str(user.id) + 'does not exist')
            villages = requesting_loop_user.get_villages()
            mandis = requesting_loop_user.get_mandis()
            Log = get_model('loop', 'Log')
            Farmer = get_model('loop', 'Farmer')
            Mandi = get_model('loop', 'Mandi')
            Gaddidar = get_model('loop', 'Gaddidar')
            GaddidarCommission = get_model('loop','GaddidarCommission')
            Transporter = get_model('loop', 'Transporter')
            TransportationVehicle = get_model('loop', 'TransportationVehicle')
            State = get_model('loop','State')
            list_rows = []
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,model_id=requesting_loop_user.id,entry_table__in=['LoopUser']))
            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,model_id=requesting_loop_user.village.block.district.state.id,entry_table__in=['State']))
            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, entry_table__in=['Crop', 'Vehicle']))
            village_list_queryset = Log.objects.filter(
                timestamp__gt=timestamp, loop_user=requesting_loop_user, entry_table__in=['Village'])
            list_rows.append(village_list_queryset)

            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, village__in=villages, entry_table__in=['Farmer']))

            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,
                                                loop_user__village__block_id=requesting_loop_user.village.block.id,
                                                entry_table__in=[
                                                    'Transporter']))

            list_rows.append(Log.objects.filter(timestamp__gt=timestamp,
                                                loop_user__village__block_id=requesting_loop_user.village.block.id,
                                                entry_table__in=[
                                                    'TransportationVehicle']))

            transporter_trans_vehicle_rows = Log.objects.filter(timestamp__gt=timestamp, entry_table__in=[
                'Transporter', 'TransportationVehicle'])

            for entry in transporter_trans_vehicle_rows:
                if entry.entry_table == "Transporter" and entry.loop_user == None:
                    if entry.action != -1 and Transporter.objects.get(id=entry.model_id).block.id == requesting_loop_user.village.block.id:
                        list_rows.append(entry)
                    elif entry.action == -1:
                        list_rows.append(entry)
                elif entry.entry_table == "TransportationVehicle" and entry.loop_user == None:
                    if entry.action != -1 and TransportationVehicle.objects.get(
                            id=entry.model_id).transporter.block.id == requesting_loop_user.village.block.id:
                        list_rows.append(entry)
                    elif entry.action == -1:
                        list_rows.append(entry)

            mandi_list_queryset = Log.objects.filter(
                timestamp__gt=timestamp, loop_user=requesting_loop_user, entry_table__in=['Mandi'])
            list_rows.append(mandi_list_queryset)

            gaddidar_rows = Log.objects.filter(
                timestamp__gt=timestamp, entry_table__in=['Gaddidar'])
            for grow in gaddidar_rows:
                if grow.action !=-1 and Gaddidar.objects.get(id=grow.model_id).mandi in mandis:
                    list_rows.append(grow)
                elif grow.action == -1:
                    list_rows.append(grow)

            gaddidar_commission_rows = Log.objects.filter(
                timestamp__gt=timestamp,entry_table__in=['GaddidarCommission'])
            for gcrow in gaddidar_commission_rows:
                list_rows.append(gcrow)

            list_rows.append(Log.objects.filter(
                timestamp__gt=timestamp, loop_user=requesting_loop_user, entry_table__in=['CombinedTransaction']))

            list_rows.append(
                Log.objects.filter(timestamp__gt=timestamp, loop_user=requesting_loop_user, entry_table__in=['DayTransportation']))

            village_farmer_list = []
            for village in village_list_queryset:
                if village.action == 1:
                    village_wise_farmer_list = Farmer.objects.filter(
                        village__id=village.model_id)
                    for farmer in village_wise_farmer_list:
                        obj = Log(action=1,
                                  entry_table="Farmer", model_id=farmer.id)
                        village_farmer_list.append(obj)

            list_rows.append(village_farmer_list)

            mandi_gaddidar_list = []
            for mandi in mandi_list_queryset:
                if mandi.action == 1:
                    mandi_wise_gaddidar_list = Gaddidar.objects.filter(
                        mandi__id=mandi.model_id)
                    for gaddidar in mandi_wise_gaddidar_list:
                        obj = Log(action=1,
                                  entry_table="Gaddidar", model_id=gaddidar.id)
                        mandi_gaddidar_list.append(obj)

            list_rows.append(mandi_gaddidar_list)
            data_list = []

            for row in list_rows:
                if row:
                    try:
                        for i in row:
                            data_list.append(get_log_object(i))
                    except TypeError, te:
                        data_list.append(get_log_object(row))
            if list_rows:
                data = json.dumps(data_list, cls=DatetimeEncoder)
                return HttpResponse(data, content_type="application/json")
    return HttpResponse("0")
