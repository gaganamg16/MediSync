from django.urls import path
from . import views

urlpatterns = [
path("", views.record_list, name="record_list"),
path("add/", views.add_record, name="add_record"),
path("edit/<int:id>/", views.edit_record, name="edit_record"),
path("delete/<int:id>/", views.delete_record, name="delete_record"),
path("download-pdf/", views.download_records_pdf, name="download_records_pdf"),
]
