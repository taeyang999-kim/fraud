import numpy as np
import tensorflow as tf
import joblib

# =========================
# 📦 모델 로드
# =========================
model = tf.keras.models.load_model("models/autoencoder.h5")
scaler = joblib.load("models/scaler.pkl")

# =========================
# 🔍 예측 함수
# =========================
def predict_fraud(input_data):
    data_scaled = scaler.transform([input_data])

    recon = model.predict(data_scaled)

    error = np.mean(np.square(data_scaled - recon))

    return error