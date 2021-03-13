from django.urls import path
from notes import views

urlpatterns = [
        path('', views.index,name='temp2'),
        path('', views.drive_auth, name="drive_auth"),
]