from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin import SimpleListFilter

from models import *

class hack4farmingAdmin(AdminSite):
	def has_permission(self, request):
		return request.user.is_active

class FarmerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phonenumber')

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phonenumber')

class RequirementAdmin(admin.ModelAdmin):
	list_display = ('id','date','requesttype', 'requirementclass','requirementvariety','quantity','unit')

class QuotationAdmin(admin.ModelAdmin):
	list_display = ('id','date', 'requirementclass','quantity' ,'price' ,'pickupdate')

hack4farming_admin = hack4farmingAdmin(name = 'hack4farming_admin')

hack4farming_admin.register(Farmer,FarmerAdmin)
hack4farming_admin.register(Supplier,SupplierAdmin)
hack4farming_admin.register(Requirement,RequirementAdmin)
hack4farming_admin.register(Quotation,QuotationAdmin)