from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from order import views

urlpatterns = patterns('',
    url(r'^$', views.OrderList.as_view()),
    url(r'^([0-9]+)/$', views.OrderDetail.as_view()),
    url(r'^item/$', views.ItemList.as_view()),
    url(r'^item/([0-9]+)/$', views.ItemDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)