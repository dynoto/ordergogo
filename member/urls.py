from django.conf.urls import patterns, url
# from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework.authtoken.views import ObtainAuthToken
from member import views
from location import views as locationViews

urlpatterns = patterns('',
    url(r'^register/$', views.Register.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^verify/$', views.Verify.as_view()),
    url(r'^$', views.MemberDetail.as_view()),
    url(r'^photo/$', views.MemberPhotoList.as_view()),
    url(r'^category/$', views.MemberCategoryList.as_view()),
    url(r'^category/([0-9]+)/$', views.MemberCategoryDetail.as_view()),
    url(r'^address/$', locationViews.MemberAddressList.as_view()),
    url(r'^address/([0-9]+)/$', locationViews.MemberAddressDetail.as_view()),
    url(r'^referral/$', views.MemberReferralDetail.as_view()),
)