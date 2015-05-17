from django.conf.urls import patterns, url
# from rest_framework.urlpatterns import format_suffix_patterns
from credit import views
from rest_framework import routers

r = routers.SimpleRouter()
r.register(r'package', views.PackageViewSet)

# urlpatterns = patterns('',
#     # url(r'^$', views.CreditDetail.as_view()),
    
# )
urlpatterns = r.urls