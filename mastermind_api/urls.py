#-*- coding: utf-8 -*-
from django.conf.urls import url, include

urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^', include(u'core.urls')),
]
