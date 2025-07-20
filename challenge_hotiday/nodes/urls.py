from django.urls import path
from . import views

app_name = 'nodes'

urlpatterns = [
    # API endpoints
    path('api/nodes/', views.list_all_nodes, name='list_all_nodes'),
    path('api/nodes/<int:node_id>/', views.get_node, name='get_node'),
    path('api/nodes/<int:node_id>/children/', views.search_children, name='search_children'),
    path('api/nodes/', views.create_node, name='create_node'),
] 