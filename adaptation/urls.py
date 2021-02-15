from django.urls import path
from . import views

app_name = 'adaptation'

urlpatterns = [
    path('', views.map_list, name='all_maps'),
    path('<int:map_id>/', views.map_detail, name='map_detail'),
    # path('<int:quiz_id>/answer/', views.quiz_answer, name='quiz_answer'),
]
