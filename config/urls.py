from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),
    path("medicines/", include("medicines.urls")),
    path("appointments/", include("appointments.urls")),
    path("records/", include("records.urls")),

    path("ai-assistant/", include("ai_assistant.urls")),
]