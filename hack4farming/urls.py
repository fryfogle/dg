from django.conf.urls import patterns, url

from hack4farming import views

urlpatterns = patterns('',
                      
                       url(r'^requirements/$', views.Requirementrequest),
                       url(r'^farmers/$', views.Farmerrequest),
                       url(r'^quotations/$', views.Quotationrequest),
                       )