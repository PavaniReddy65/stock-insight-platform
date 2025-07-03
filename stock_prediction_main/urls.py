from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse
from django.shortcuts import redirect

# 🩺 Health check endpoint
def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),  # All custom endpoints
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("healthz/", health_check),
    path("", lambda request: redirect("dashboard")),  # 👈 Redirect root URL to dashboard
]
