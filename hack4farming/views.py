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
    if request.method == "POST":
        body = json.loads(request.body)
        farmer=Farmer(name=body["name"],phonenumber=body["phonenumber"],village=body["village"],pincode=body["pincode"],latitude=body["latitude"],longitude=body["longitude"],landsize=body["landsize"])
        farmer.save()
        return HttpResponse(json.dumps({"id":farmer.id}))
    elif request.method == "GET":
        farmers=list(Farmer.objects.filter().values_list('id','name','phonenumber','village','pincode','latitude','longitude','landsize'))
        resp = json.dumps([farmer for farmer in farmers])
        return HttpResponse(resp)

@csrf_exempt
def Supplierrequest(request):
    if request.method == "POST":
        body = json.loads(request.body)
        supplier=Supplier(name=body["name"],phonenumber=body["phonenumber"],suppliercategory=body["suppliercategory"],firmname=body["firmname"],pincode=body["pincode"],latitude=body["latitude"],longitude=body["longitude"])
        supplier.save()
        return HttpResponse(json.dumps({"id":supplier.id}))
    elif request.method == "GET":
        suppliers=list(Supplier.objects.filter().values_list('id','name','phonenumber','suppliercategory','firmname','pincode','latitude','longitude'))
        resp = json.dumps([supplier for supplier in suppliers])
        return HttpResponse(resp)

    #return render_to_response()
@csrf_exempt
def Requirementrequest(request):
    #farmer = request.GET.get('farmerid')
    if request.method == "POST":
        body = json.loads(request.body)
        farmerObject = Farmer.objects.filter(id=body['farmer'])
        requirement = Requirement(date=body['date'],farmer=farmerObject,requesttype=body['requesttype'],requirementclass=body['requirementclass'],buyrent=body['buyrent'],requirementcrop=body['requirementcrop'],requirementvariety=body['requirementvariety'],quantity=body['quantity'],unit=body['unit'])
        requirement.save()
    elif request.method == "GET":
        requirements = list(Requirement.objects.filter().values_list('id','date','farmer__name','requesttype','requirementclass','buyrent','requirementcrop','requirementvariety','quantity','unit'))
        resp = json.dumps([requirement for requirement in requirements])
        return HttpResponse(resp)


@csrf_exempt
def Quotationrequest(request):
    if request.method == "POST":
        body = json.loads(request.body)
        supplierObject = Supplier.objects.filter(id=body['supplier'])
        quotation = Quotation(date=body['date'],supplier=supplierObject,requirementclass=body['requirementclass'],requirementcrop=body['requirementcrop'],requirementvariety=body['requirementvariety'],quantity=body['quantity'],price=body['price'],pickupdate=body['pickupdate'])
        quotation.save()
    elif request.method == "GET":
        quotations = list(Quotation.objects.filter().values_list('id','date','supplier__id','requirementclass','requirementcrop','requirementvariety','quantity','price','pickupdate'))
        resp = json.dumps([quotation for quotation in quotations])
        return HttpResponse(resp)