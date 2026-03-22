from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")),
    path("accounts/", include("accounts.urls")),
    path("assets/", include("assets.urls")),
    path("", RedirectView.as_view(url="/assets/")),
]
