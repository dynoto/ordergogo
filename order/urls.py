from django.conf.urls import patterns, url
from order import views

urlpatterns = patterns('',
    url(r'^$', views.OrderList.as_view()),
    url(r'^([0-9]+)/$', views.OrderDetail.as_view()),
    url(r'^([0-9]+)/assign/$', views.OrderAssign.as_view()),

)