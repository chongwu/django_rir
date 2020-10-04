from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.departments_list, name='departments_list'),
    path('departments/<int:department_id>/persons/', views.person_list, name='person_list'),
    path('persons/<int:person_id>/', views.person_detail, name='person_detail'),
    path('persons/<int:person_id>/questionnaire/', views.create_questionnaire, name='person_create_questionnaire'),
    path('persons/<int:person_id>/questionnaire/upload',
         views.upload_questionnaire,
         name='person_upload_questionnaire'),
    path('persons/<int:person_id>/questionnaire/download',
         views.download_questionnaire,
         name='person_download_questionnaire'),
]
