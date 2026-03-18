from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("recursos/", views.resource_list, name="resource_list"),
    path("recursos/nuevo/", views.resource_create, name="resource_create"),
    path("recursos/<int:pk>/editar/", views.resource_update, name="resource_update"),
    path("recursos/<int:pk>/eliminar/", views.resource_delete, name="resource_delete"),
    path("categorias/", views.category_list, name="category_list"),
    path("categorias/nueva/", views.category_create, name="category_create"),
    path("categorias/<int:pk>/editar/", views.category_update, name="category_update"),
    path("categorias/<int:pk>/eliminar/", views.category_delete, name="category_delete"),
]
