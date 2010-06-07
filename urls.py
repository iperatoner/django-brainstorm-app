from django.conf.urls.defaults import *
from django.contrib import admin

import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('brainstorm.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root' : settings.MEDIA_ROOT, 'show_indexes' : True })
)
