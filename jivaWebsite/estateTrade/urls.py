from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.et_index, name='et_index'),
    url(r'^trend$', views.et_trend, name='et_trend'),
    url(r'^trend_compare$', views.et_trend_compare, name='et_trend_compare'),
]
