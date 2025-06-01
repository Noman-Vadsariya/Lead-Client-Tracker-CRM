from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('leads/', views.lead_list, name='lead_list'),
]
