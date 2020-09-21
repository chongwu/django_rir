from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.person_list, name='person_list'),
    path('<int:person_id>/', views.person_detail, name='person_detail'),
    path('<int:person_id>/questionnaire/', views.create_questionnaire, name='person_create_questionnaire'),
    path('<int:person_id>/questionnaire/upload', views.upload_questionnaire, name='person_upload_questionnaire'),
    path('<int:person_id>/questionnaire/download', views.download_questionnaire, name='person_download_questionnaire'),
]
