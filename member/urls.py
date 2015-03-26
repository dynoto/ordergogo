from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework.authtoken.views import ObtainAuthToken
from member import views

urlpatterns = patterns('',
    # url(r'^register/$', views.Register.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^profile/$', views.Profile.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)