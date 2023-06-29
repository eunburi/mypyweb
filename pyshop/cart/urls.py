from django.urls import path

from cart import views

appname = 'cart'

urlpatterns = [
    path('', views.detail, name='detail'),

]

