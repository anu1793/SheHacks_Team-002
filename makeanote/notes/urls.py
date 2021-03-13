from django.urls import path
from django.conf.urls import url, include
from . import views
app_name = 'notes'
urlpatterns = [
    url(r'^api/v1/get_meaning', views.index, name='index'),
    
]