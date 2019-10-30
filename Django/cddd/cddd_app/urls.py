
from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('',views.ip,name='ip'),
    path('disp/',views.disp,name='d'),
]
