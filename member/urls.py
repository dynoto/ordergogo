from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework.authtoken.views import ObtainAuthToken
from member import views

urlpatterns = patterns('',
    # url(r'^register/$', views.Register.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^member/$', views.MemberDetail.as_view()),
    url(r'^member/photo/$', views.MemberPhoto.as_view()),
    url(r'^member/category/$', views.MemberCategory.as_view()),
    url(r'^member/category/(?<mc_id>[0-9]+)/$', views.MemberCategory.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)