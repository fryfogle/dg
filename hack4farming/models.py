from django.db import models
from django.utils import timezone
import datetime

REQUEST_TYPE = ((0, "Personal"), (1, "Group"))
REQUIREMENT_CLASS = ((0, "Seed"), (1, "Fertilizer") , (2, "Loan") , (3, "Equipments"))
BUY_RENT = ((0, "Buy"), (1, "Rent"))
UNITS = ((0, "Kg"), (1, "Rupees"), (2,"Pieces"))
SUPPLIER_CATEGORY = ((0, "Seed"), (1, "Fertilizer"), (2,"Bank"),(3,"Equipment"))

class Farmer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="default",null=True,blank=True)
    phonenumber = models.CharField(max_length=14, null=True, blank=True, default="0")
    village = models.CharField(max_length=30, default=None, null=True)
    pincode = models.CharField(max_length=8, null=True, blank=True, default="0")
    latitude = models.CharField(max_length=15, null=True, blank=True, default="0")
    longitude = models.CharField(max_length=15, null=True, blank=True, default="0")
    landsize = models.CharField(max_length=5, null=True, blank=True, default="0")

    def __unicode__(self):
        return '%s' %(self.name)

class Requirement(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=25,null=True, blank=True)
    requesttype = models.CharField(max_length=25,null=True, blank=True)
    farmer = models.ForeignKey(Farmer,null=True)
    requirementclass = models.CharField(max_length=25,null=True, blank=True)
    buyrent = models.CharField(max_length=25,null=True, blank=True)
    requirementcrop = models.CharField(max_length=25, null=True, blank=True, default="0")
    requirementvariety = models.CharField(max_length=25, null=True, blank=True, default="0")
    quantity = models.IntegerField(null=True,blank=True,default=0)
    unit = models.CharField(max_length=25,null=True, blank=True)

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="default")
    phonenumber = models.CharField(
        max_length=14, null=True, blank=True, default="0")
    suppliercategory = models.CharField(max_length=25,null=True, blank=True)
    firmname = models.CharField(
        max_length=50, null=True, blank=True, default="0")
    pincode = models.CharField(
        max_length=8, null=True, blank=True, default="0")
    latitude = models.CharField(max_length=15, null=True, blank=True, default="0")
    longitude = models.CharField(max_length=15, null=True, blank=True, default="0")

class Quotation(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=25,null=True, blank=True)
    supplier = models.ForeignKey(Supplier,null=True)
    requirementclass = models.CharField(max_length=25,null=True, blank=True)
    requirementcrop = models.CharField(max_length=25, null=True, blank=True, default="0")
    requirementvariety = models.CharField(max_length=25, null=True, blank=True, default="0")
    quantity = models.IntegerField(null=True,blank=True,default=0)
    price = models.FloatField(null=True)
    pickupdate = models.CharField(max_length=25,null=True, blank=True)

class RequirementQuotation(models.Model):
    id = models.AutoField(primary_key=True)
    requirementid = models.IntegerField()
    quotationid = models.IntegerField()
        