import os
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Prediction

# 🔍 Reusable prediction function
def run_prediction(ticker):
    df = yf.download(ticker, period="10y")
    close_prices = df[["Close"]].values

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(close_prices)

    X, y = [], []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i-60:i, 0])
        y.append(scaled_data[i, 0])
    X = np.array(X)
    y = np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    model_path = os.getenv("MODEL_PATH", "stock_prediction_model.keras")
    model = load_model(model_path)

    predictions = model.predict(X)
    predictions = scaler.inverse_transform(predictions)
    y_actual = scaler.inverse_transform(y.reshape(-1, 1))

    mse = mean_squared_error(y_actual, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_actual, predictions)
    next_day_price = float(predictions[-1])

    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    plot1 = f"static/plot_close_{ts}.png"
    plot2 = f"static/plot_compare_{ts}.png"

    plt.figure(figsize=(10, 4))
    plt.plot(df["Close"], label="Close Price")
    plt.title("Closing Price History")
    plt.legend()
    plt.savefig(plot1)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(y_actual, label="Actual")
    plt.plot(predictions, label="Predicted")
    plt.title("Actual vs Predicted")
    plt.legend()
    plt.savefig(plot2)
    plt.close()

    user = User.objects.first()
    if not user:
        raise Exception("No user found. Please create one with `createsuperuser`.")

    Prediction.objects.create(
        user=user,
        ticker=ticker,
        predicted_price=next_day_price,
        mse=mse,
        rmse=rmse,
        r2=r2,
        plot_url_1=plot1,
        plot_url_2=plot2,
    )

    return {
        "ticker": ticker,
        "predicted_price": next_day_price,
        "mse": mse,
        "rmse": rmse,
        "r2": r2,
        "plot_url_1": plot1,
        "plot_url_2": plot2,
        "status": "ok",
    }


# 🛠️ Django CLI Command for direct execution
class Command(BaseCommand):
    help = "Run prediction for given ticker"

    def add_arguments(self, parser):
        parser.add_argument("--ticker", type=str, help="Ticker symbol")
        parser.add_argument("--all", action="store_true", help="Run for all tickers")

    def handle(self, *args, **kwargs):
        ticker = kwargs.get("ticker")
        run_all = kwargs.get("all")

        if not ticker and not run_all:
            self.stdout.write(self.style.ERROR("You must specify --ticker or --all"))
            return

        tickers = [ticker] if ticker else ["TSLA", "AAPL", "MSFT"]

        for tk in tickers:
            self.stdout.write(f"\n📈 Predicting for: {tk}")
            try:
                result = run_prediction(tk)
                self.stdout.write(self.style.SUCCESS(
                    f"✅ Success: {tk} → {result['predicted_price']:.2f}"
                ))
                self.stdout.write(f"🖼️ Plots:\n - {result['plot_url_1']}\n - {result['plot_url_2']}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error with {tk}: {e}"))
