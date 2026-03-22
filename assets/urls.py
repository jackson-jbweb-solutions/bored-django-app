from django.urls import path

from . import views

urlpatterns = [
    path("", views.asset_list, name="asset-list"),
    path("rows/", views.asset_list_rows, name="asset-list-rows"),
    path("create-form/", views.asset_create_form, name="asset-create-form"),

    path("wheelchairs/create/", views.wheelchair_create, name="wheelchair-create"),
    path("wheelchairs/<int:pk>/edit/", views.wheelchair_edit, name="wheelchair-edit"),
    path("wheelchairs/<int:pk>/row/", views.wheelchair_row, name="wheelchair-row"),
    path("wheelchairs/<int:pk>/delete/", views.wheelchair_delete, name="wheelchair-delete"),

    path("cushions/create/", views.cushion_create, name="cushion-create"),
    path("cushions/<int:pk>/edit/", views.cushion_edit, name="cushion-edit"),
    path("cushions/<int:pk>/row/", views.cushion_row, name="cushion-row"),
    path("cushions/<int:pk>/delete/", views.cushion_delete, name="cushion-delete"),

    path("wards/", views.ward_list, name="ward-list"),
    path("wards/create/", views.ward_create, name="ward-create"),
    path("wards/<int:pk>/edit/", views.ward_edit, name="ward-edit"),
    path("wards/<int:pk>/row/", views.ward_row, name="ward-row"),
    path("wards/<int:pk>/delete/", views.ward_delete, name="ward-delete"),
]
