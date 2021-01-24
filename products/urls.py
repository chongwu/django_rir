from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_list, name='all_products'),
    path('upload/', views.upload_products_list, name='upload_products_list'),
    path('<int:product_id>/', views.view_product, name='view_product'),
    path('<int:product_id>/projects/upload/', views.upload_projects_list, name='upload_projects_list'),
    path('<int:product_id>/projects/<int:project_id>/', views.view_project, name='view_project'),
]


