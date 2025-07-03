from django.urls import path
from api.views import (
    healthz,
    simple_predict,
    RegisterView,
    PredictStockView,
    PredictionListView,
    DashboardTemplateView
)

urlpatterns = [
    # 🩺 Docker or system health check
    path("healthz/", healthz, name="healthz"),

    # 🔍 Static test prediction
    path("simple-predict/", simple_predict, name="simple-predict"),

    # 🔐 JWT-secured endpoints
    path("register/", RegisterView.as_view(), name="register"),
    path("predict/", PredictStockView.as_view(), name="predict"),
    path("predictions/", PredictionListView.as_view(), name="predictions"),

    # 🎨 Dashboard (HTML template served with Tailwind)
    path("dashboard/", DashboardTemplateView.as_view(), name="dashboard"),
]
