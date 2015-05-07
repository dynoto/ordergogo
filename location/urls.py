from django.conf.urls import patterns, url
# from rest_framework.urlpatterns import format_suffix_patterns
from location import views

urlpatterns = patterns('',
    url(r'^address/$', views.MemberAddressList.as_view()),
    url(r'^address/([0-9]+)/$', views.MemberAddressDetail.as_view()),
    # url(r'^area/$', views.AreaList.as_view()),
    # url(r'^area/([0-9]+)/$', views.AreaDetail.as_view()),
)