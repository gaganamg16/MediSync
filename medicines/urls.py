from django.urls import path
from . import views

urlpatterns = [
    # Medicine pages
    path("", views.medicine_list, name="medicine_list"),
    path("add/", views.add_medicine, name="add_medicine"),
    path("edit/<int:id>/", views.edit_medicine, name="edit_medicine"),
    path("delete/<int:id>/", views.delete_medicine, name="delete_medicine"),
    path("reminders/", views.medicine_reminders, name="medicine_reminders"),

    # Prescription pages
    path("prescriptions/add/", views.add_prescription, name="add_prescription"),
    path("prescriptions/", views.prescription_list, name="prescription_list"),
]