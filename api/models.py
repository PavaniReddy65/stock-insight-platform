from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    predicted_price = models.FloatField()
    mse = models.FloatField()
    rmse = models.FloatField()
    r2 = models.FloatField()
    plot_url_1 = models.CharField(max_length=255)
    plot_url_2 = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticker} prediction by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"
