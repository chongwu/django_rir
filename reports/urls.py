from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list, name='all_reports'),
    path('corporate/', views.corporate_report, name='corporate_report'),
    path('department/<int:department_id>', views.department_report, name='department_report'),
]
