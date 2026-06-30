import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from model import build_autoencoder

# =========================
# 📥 데이터 불러오기
# =========================
df = pd.read_csv("data/PS_20174392719_1491204439457_log.csv")

# =========================
# 🎯 사용할 숫자 컬럼만 선택
# =========================
features = [
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest"
]

X = df[features]

# =========================
# 📊 스케일링 (중요)
# =========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# 🚨 정상 데이터만 학습
# =========================
X_train = X_scaled[df["isFraud"] == 0]

print("정상 데이터 개수:", len(X_train))

# =========================
# 🧠 모델 생성
# =========================
model = build_autoencoder(input_dim=X_train.shape[1])

# =========================
# 🎓 학습
# =========================
model.fit(
    X_train,
    X_train,
    epochs=10,
    batch_size=32,
    validation_split=0.1
)

# =========================
# 💾 저장
# =========================
model.save("models/autoencoder.h5")
joblib.dump(scaler, "models/scaler.pkl")

print("✅ 학습 완료!")