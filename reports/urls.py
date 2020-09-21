from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.corporate_report, name='corporate_report'),
    path('department/', views.department_report, name='department_report'),
]
