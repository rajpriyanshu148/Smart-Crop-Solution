from flask import Flask, render_template, request
import pickle
import pandas as pd
import os

app = Flask(__name__)

# -------- Safe model loading (Render compatible) --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

crop_model_path = os.path.join(BASE_DIR, "models", "crop_recommendation_model.pkl")
yield_model_path = os.path.join(BASE_DIR, "models", "crop_yield_model.pkl")

with open(crop_model_path, "rb") as f:
    crop_model = pickle.load(f)

with open(yield_model_path, "rb") as f:
    yield_model = pickle.load(f)

# --------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # -------- Form Data --------
        N = float(request.form["N"])
        P = float(request.form["P"])
        K = float(request.form["K"])
        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])
        ph = float(request.form["ph"])
        rainfall = float(request.form["rainfall"])
        state = request.form["state"]
        season = request.form["season"]

        # -------- Crop Prediction --------
        crop_input = pd.DataFrame(
            [[N, P, K, temperature, humidity, ph, rainfall]],
            columns=["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
        )

        crop = crop_model.predict(crop_input)[0]

        # -------- Yield Prediction --------
        yield_input = pd.DataFrame(
            [[state, crop, season, 5, rainfall, 150]],
            columns=["State", "Crop", "Season", "Area", "Annual_Rainfall", "Fertilizer"]
        )

        predicted_yield = round(float(yield_model.predict(yield_input)[0]), 2)

        return render_template(
            "index.html",
            crop=crop,
            predicted_yield=predicted_yield
        )

    except Exception as e:
        return render_template(
            "index.html",
            error=str(e)
        )

