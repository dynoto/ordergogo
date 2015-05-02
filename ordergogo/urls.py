from django.http import HttpResponse
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ordergogo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^member/', include('member.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^vendor/', include('vendor_order.urls')),
    url(r'^location/', include('location.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain"))
)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]