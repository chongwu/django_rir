from django.urls import path
from . import views

app_name = 'adaptation'

urlpatterns = [
    path('', views.map_list, name='all_maps'),
    path('<int:map_id>/', views.map_detail, name='map_detail'),
    path('getPositions/', views.get_positions_by_type),
    path('map-point/<int:point_id>/add-data/', views.save_map_point_data),
    path('<int:map_id>/add-map-point/<int:point_type>/', views.add_map_point, name='add_map_point'),
    path('<int:map_id>/add-map-conclusion/<int:conclusion_type>/', views.add_map_conclusion, name='add_map_conclusion'),
    path('<int:map_id>/edit-map-conclusion/<int:conclusion_id>/', views.edit_map_conclusion, name='edit_map_conclusion'),
    path('<int:map_id>/export/', views.export, name='export'),
    # path('<int:quiz_id>/answer/', views.quiz_answer, name='quiz_answer'),
]
