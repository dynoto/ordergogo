from django.http import HttpResponse
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.authtoken import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ordergogo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^member/', include('member.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^location/', include('location.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-token-auth/', views.obtain_auth_token),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain"))
)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]