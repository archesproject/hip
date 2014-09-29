import settings as package_settings
from django.conf.urls import patterns, url
import os

def get_urlpatterns(prefix=None):
    packagename = package_settings.ROOT_DIR.split(os.sep)[-1]

    urlpatterns =  patterns('',
    	url(r'^Arches/$', 'archesproject.packages.%s.views.main.index' % packagename),
    )

    return urlpatterns
