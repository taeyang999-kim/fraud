import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
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

# =========================
# 🚨 정상 거래만 추출
# =========================
normal_df = df[df["isFraud"] == 0]

X_train, X_test = train_test_split(
    normal_df[features],
    test_size=0.2,
    random_state=42
)

# =========================
# 📊 스케일러는 학습 데이터만 사용
# =========================
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("학습 데이터 :", len(X_train))
print("테스트 데이터 :", len(X_test))

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

X_pred = model.predict(X_test)

mse = np.mean(np.square(X_test - X_pred), axis=1)

threshold = np.percentile(mse, 95)

joblib.dump(threshold, "models/threshold.pkl")
np.save("models/mse.npy", mse)

print("Threshold :", threshold)
print("평균 MSE :", np.mean(mse))