from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.departments_list, name='departments_list'),
    path('departments/<int:department_id>/', views.person_list, name='person_list'),
    # path('departments/<int:department_id>/upload/', views.upload_persons_list, name='upload_persons_list'),
    path('departments/upload/', views.upload_department_list, name='upload_department_list'),
    path('departments/positions/upload/', views.upload_positions_list, name='upload_positions_list'),
    path('departments/matrix/', views.export_employees_xlsx, name='export_all_employees_xlsx'),
    path('departments/matrix/<int:department_id>/', views.export_employees_xlsx, name='export_employees_xlsx'),
    path('persons/<int:person_id>/', views.person_detail, name='person_detail'),
    path('persons/<int:person_id>/questionnaire/', views.create_questionnaire, name='person_create_questionnaire'),
    path('persons/<int:person_id>/questionnaire/upload/',
         views.upload_questionnaire,
         name='person_upload_questionnaire'),
    path('persons/<int:person_id>/questionnaire/download/',
         views.download_questionnaire,
         name='person_download_questionnaire'),
    path('persons/<int:person_id>/matrix/download/', views.export_employee_matrix, name='export_employee_matrix'),
    path('json/users/', views.json_users, name='json_users'),
    path('json/persons/', views.json_persons, name='json_persons'),
    path('json/departments/', views.json_departments, name='json_departments'),
    path('json/positions/', views.json_positions, name='json_positions'),
]
