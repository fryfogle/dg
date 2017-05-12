import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from hack4farming.models import *
import requests


@csrf_exempt
def Farmerrequest(request):
    pass
    #if request.method == "POST":
    #    farmer =  Farmer(name=request.body["name"],phonenumber=request.body["phonenumber"],village)


    #return render_to_response()
@csrf_exempt
def Requirementrequest(request):
    #farmer = request.GET.get('farmerid')
    if request.method == "GET":
        requirements = list(Requirement.objects.filter().values_list('id','date','requesttype','requirementclass','buyrent','requirementcrop','requirementvariety','quantity','unit'))
        print requirements
        resp = json.dumps([requirement for requirement in requirements])
        print resp
        return HttpResponse(resp)

@csrf_exempt
def Quotationrequest(request):
    if request.method == "GET":
        quotations = Quotations.objects.all()
        resp = json.dumps([quotation for quotation in quotations])
        return HttpResponse(resp)