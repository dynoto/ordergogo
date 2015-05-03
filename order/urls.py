from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from order import views
from django.conf.urls import include

urlpatterns = patterns('',
    url(r'^$', views.OrderList.as_view()),
    url(r'^([0-9]+)/$', views.OrderDetail.as_view()),
    url(r'^([0-9]+)/assign/$', views.OrderAssign.as_view()),
    url(r'^vendor/', include('order.vendor_urls')),

)