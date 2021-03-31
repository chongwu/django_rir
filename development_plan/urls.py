from django.urls import path
from . import views

app_name = 'development_plan'

urlpatterns = [
    # path('', views.map_list, name='all_maps'),
    path('<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path('<int:plan_id>/export/', views.plan_export, name='plan_export'),
    # path('getPositions/', views.get_positions_by_type),
    # path('map-point/<int:point_id>/add-data/', views.save_map_point_data),
    # path('<int:quiz_id>/answer/', views.quiz_answer, name='quiz_answer'),
]
