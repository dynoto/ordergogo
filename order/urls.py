from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from order import views
from django.conf.urls import include

urlpatterns = patterns('',
    url(r'^$', views.OrderList.as_view()),
    url(r'^([0-9]+)/$', views.OrderDetail.as_view()),
    url(r'^([0-9]+)/assign/$', views.OrderAssign.as_view()),
    url(r'^vendor/', include('order_vendor.urls')),
    # url(r'^([0-9]+)/reject/$', views.OrderReject.as_view()),
    # url(r'^([0-9]+)/status/$', views.OrderStatusChange.as_view()),
    # url(r'^track/([\d\w]{0,64})/$', views.OrderTrack.as_view()),
    # url(r'^item/$', views.ItemList.as_view()),
    # url(r'^item/([0-9]+)/$', views.ItemDetail.as_view()),
    # url(r'^item/([0-9]+)/photo/$', views.PhotoList.as_view()),
    # url(r'^item/([0-9]+)/photo/([0-9]+)$', views.PhotoList.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)