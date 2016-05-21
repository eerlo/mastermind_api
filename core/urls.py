#-*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

from core.views import CreateNewGameView, MakeNewGuessView


router = routers.DefaultRouter()
router.register(r'games', CreateNewGameView, base_name=u'games')
router.register(r'guess', MakeNewGuessView, base_name=u'guesses')

urlpatterns = [
    url(r'^', include(router.urls))
]