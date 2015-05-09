from django.conf.urls import patterns, url
from order import vendor_views as views

urlpatterns = patterns('',
    url(r'^pending/$', views.OrderPendingList.as_view()),
    url(r'^assigned/$', views.OrderAssignedList.as_view()),
    url(r'^([0-9]+)/$', views.OrderDetail.as_view()),
    url(r'^([0-9]+)/bid/$', views.OrderBidDetail.as_view()),
)