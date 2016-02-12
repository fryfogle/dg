import json

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.db.models import Count, Min, Sum, Avg, Max

from tastypie.models import ApiKey, create_api_key
from models import LoopUser, CombinedTransaction, LoopUser

from loop_data_log import get_latest_timestamp

# Create your views here.
HELPLINE_NUMBER = "09891256494"

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        loop_user = LoopUser.objects.filter(user = user)
        if user is not None and user.is_active and loop_user.count() > 0:
            auth.login(request, user)
            try:
                api_key = ApiKey.objects.get(user=user)
            except ApiKey.DoesNotExist:
                api_key = ApiKey.objects.create(user=user)
                api_key.save()
            log_object = get_latest_timestamp()
            return HttpResponse(json.dumps({'key':api_key.key, 'timestamp' : str(log_object.timestamp), 'full_name':loop_user[0].name, 'mode' : loop_user[0].mode, 'helpline' : HELPLINE_NUMBER, 'phone_number': loop_user[0].phone_number }))
        else:
            return HttpResponse("0", status=401 )
    else:
        return HttpResponse("0", status = 403)
    return HttpResponse("0", status=400)

def home(request):
	print request
	return render_to_response(request, 'loop_base.html')

def dashboard(request):
    return render(request, 'loop/loop_dashboard.html')

def village_wise_data(request):
    #start_date = request.POST['start_date']
    #end_date = request.POST['end_date']
    start_date = '2016-01-01'
    end_date = '2016-01-31'
    transactions = CombinedTransaction.objects.filter(date__range = [start_date, end_date]).values('farmer__village__village_name').distinct().annotate(Count('farmer', distinct = True), Sum('amount'), Sum('quantity'), Count('date', distinct = True))
    data = json.dumps(list(transactions))
    return HttpResponse(data)

def mediator_wise_data(request):
    #start_date = request.POST['start_date']
    #end_date = request.POST['end_date']
    start_date = '2016-01-01'
    end_date = '2016-01-31'
    transactions = list(CombinedTransaction.objects.filter(date__range = [start_date, end_date]).values('user_created__id').distinct().annotate(Count('farmer', distinct = True), Sum('amount'), Sum('quantity'), Count('date', distinct = True)))
    for i in transactions:
        user = LoopUser.objects.get(user_id = i['user_created__id'])
        i['user_name'] = user.name
    data = json.dumps(transactions)
    return HttpResponse(data)

def crop_wise_data(request):
    #start_date = request.POST['start_date']
    #end_date = request.POST['end_date']
    start_date = '2015-01-01'
    end_date = '2017-01-31'
    # crop wise data here
    crops = CombinedTransaction.objects.filter(date__range = [start_date, end_date]).values_list('crop__crop_name', flat=True).distinct()
    transactions = CombinedTransaction.objects.filter(date__range = [start_date, end_date]).values('crop__crop_name', 'date').distinct().annotate(Sum('amount'), Sum('quantity'))
    # crop and mediator wise data
    crops_mediators = CombinedTransaction.objects.filter(date__range = [start_date, end_date]).values('crop__crop_name','user_created__id').distinct().annotate(amount = Sum('amount'), quantity = Sum('quantity'))
    crops_mediators_transactions = CombinedTransaction.objects.filter(date__range = [start_date, end_date]).values('crop__crop_name','user_created__id','date').distinct().annotate(amount = Sum('amount'), quantity = Sum('quantity'))
    for crop_mediator in crops_mediators:
        user = LoopUser.objects.get(user_id = crop_mediator['user_created__id'])
        crop_mediator['user_name'] = user.name
    dates = CombinedTransaction.objects.filter(date__range = [start_date, end_date]).values_list('date', flat=True).distinct().order_by('date').annotate(Count('farmer',distinct = True))
    dates_farmer_count = CombinedTransaction.objects.filter(date__range = [start_date, end_date]).values('date').distinct().order_by('date').annotate(Count('farmer',distinct = True))
    chart_dict = {'dates': list(dates), 'crops': list(crops), 'transactions': list(transactions), 'farmer_count' : list(dates_farmer_count), 'crops_mediators' : list(crops_mediators), 'crops_mediators_transactions' : list(crops_mediators_transactions)}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)
