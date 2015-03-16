from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import ObtainAuthToken
from member import views

urlpatterns = patterns('',
    url(r'^register/$', views.Register.as_view()),
    url(r'^login/$', views.Login.as_view()),
    # url(r'^delete/$', views.Delete.as_view()),
    # url(r'^profile/$', views.ManageProfile.as_view()),
    # url(r'^reset/$', views.ResetPassword.as_view()),
    # url(r'^languages/$', views.LanguageList.as_view()),
    # url(r'^countries/$', views.CountryList.as_view()),
    # url(r'^currencies/$', views.CurrencyList.as_view()),
    # url(r'^social_login/(?P<backend>[^/]+)/', views.SocialLogin.as_view()),
    # url(r'^social_logout/', views.SocialLogout.as_view()),
    # url(r'^register_push/$', views.RegisterPush.as_view()),
    # url(r'^retrieve_push/([0-9]+)/$', views.RetrievePush.as_view()),
    # url(r'^chat/', include('chat.urls',namespace='chat')),
    # url('', include('social.apps.django_app.urls', namespace='social')),
)

urlpatterns = format_suffix_patterns(urlpatterns)