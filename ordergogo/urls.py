from django.http import HttpResponse
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^member/', include('member.urls')),
    url(r'^order/customer/', include('order.urls')),
    url(r'^order/vendor/', include('order.vendor_urls')),
    url(r'^location/', include('location.urls')),
    url(r'^credit/', include('credit.urls')),
    url(r'^generic/', include('generic.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain"))
)

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

