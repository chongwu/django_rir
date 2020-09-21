from django.urls import path
from . import views

app_name = 'questionnaire'

urlpatterns = [
    path('create/', views.create_questionnaire, name='create_questionnaire'),
    path('edit/<int:questionnaire_id>', views.edit_questionnaire, name='edit_questionnaire'),
    path('update/<int:questionnaire_id>', views.update_questionnaire, name='update_questionnaire'),
]
