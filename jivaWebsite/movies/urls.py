from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.movies_index, name='movies_index'),
    url(r'^get_movie_link$', views.get_movie_link, name='get_movie_link'),
]