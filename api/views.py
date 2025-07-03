from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Prediction
from .serializers import RegisterSerializer, PredictionSerializer
from api.management.commands.run_predict import run_prediction


# ───────────────────────────────────────────────
# ✅ Health Check for Docker or Deployment
# ───────────────────────────────────────────────
def healthz(request):
    return JsonResponse({"status": "ok"})


# ───────────────────────────────────────────────
# 🔍 Simple Demo Prediction
# ───────────────────────────────────────────────
def simple_predict(request):
    result = run_prediction("AAPL")
    return JsonResponse(result)


# ───────────────────────────────────────────────
# 🔐 User Registration
# ───────────────────────────────────────────────
class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            user = User.objects.create_user(
                username=request.data['username'],
                password=request.data['password']
            )
            return Response({'message': 'User created successfully'}, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)


# ───────────────────────────────────────────────
# 📈 Stock Prediction API
# ───────────────────────────────────────────────
class PredictStockView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        ticker = request.data.get('ticker')
        if not ticker:
            return Response({"error": "Ticker is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = run_prediction(ticker)
            return Response(result)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# ───────────────────────────────────────────────
# 📊 Prediction History List
# ───────────────────────────────────────────────
class PredictionListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')

        ticker = request.query_params.get('ticker')
        date = request.query_params.get('date')

        if ticker:
            predictions = predictions.filter(ticker__iexact=ticker)
        if date:
            predictions = predictions.filter(created_at__date=date)

        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)


# ───────────────────────────────────────────────
# 🎨 Dashboard View (HTML + Tailwind)
# ───────────────────────────────────────────────
from django.views.generic import TemplateView

class DashboardTemplateView(TemplateView):
    template_name = "dashboard.html"

