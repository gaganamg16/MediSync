from django.urls import path
from . import views

urlpatterns = [
path("", views.home, name="home"),


path("register/", views.register, name="register"),

path("login/", views.user_login, name="login"),

path("logout/", views.user_logout, name="logout"),

path("dashboard/", views.dashboard, name="dashboard"),

path("doctor-dashboard/", views.doctor_dashboard, name="doctor_dashboard"),

path("profile/", views.profile, name="profile"),

path(
    "doctor-patients/",
    views.doctor_patients,
    name="doctor_patients"
),

]
