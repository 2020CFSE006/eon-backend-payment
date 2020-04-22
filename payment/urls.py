"""
In this file we added all the url reference
"""
from django.conf.urls import url
from django.urls import include

from payment.routes import router

urlpatterns = [
    url('^', include(router.urls)),
]
