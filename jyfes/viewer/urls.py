from django.conf.urls import url

from jyfes.viewer import views


urlpatterns = [
    url(r'^$', views.list_view),
]
