from django.conf.urls import patterns, url
# from rest_framework.urlpatterns import format_suffix_patterns
from location import views

urlpatterns = patterns('',
    url(r'^address/$', views.AddressList.as_view()),
    url(r'^address/([0-9]+)/$', views.AddressDetail.as_view()),
)

# urlpatterns = format_suffix_patterns(urlpatterns)