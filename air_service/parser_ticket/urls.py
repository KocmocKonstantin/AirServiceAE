from django.urls import path
from . import views

app_name = 'parser_ticket'
urlpatterns = [
    path('', views.upload_ticket, name='upload'),
    path('list/', views.ticket_list, name='ticket_list'),
]