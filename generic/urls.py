from django.conf.urls import patterns, url
# from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework.authtoken.views import ObtainAuthToken
from generic import views

urlpatterns = patterns('',
    url(r'^category/$', views.CategoryList.as_view()),
)