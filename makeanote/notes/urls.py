from django.urls import path
from django.conf.urls import url, include
from notes import views

urlpatterns = [
        url('', views.test, name='test'),
        url(r'^note/value', views.index, name='temp2'),

]