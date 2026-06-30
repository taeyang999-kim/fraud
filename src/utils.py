import joblib
import tensorflow as tf
import streamlit as st

def load_scaler(path="models/scaler.pkl"):
    """
    학습 때 저장한 StandardScaler를 불러옵니다.
    """
    try:
        scaler = joblib.load(path)
        return scaler
    except FileNotFoundError:
        print(f"❌ 스케일러 파일을 찾을 수 없습니다: {path}")
        return None

@st.cache_resource
def load_autoencoder_model(path="models/autoencoder.h5"):
    """
    학습 때 저장한 Keras Autoencoder 모델을 불러옵니다.
    💡 compile=False를 추가하여 버전 간 평가지표(metrics) 역직렬화 에러를 방지합니다.
    """
    try:
        # 이 부분이 수정되었습니다! compile=False 추가
        model = tf.keras.models.load_model(path, compile=False)
        return model
    except Exception as e:
        print(f"❌ 모델을 불러오는 중 오류 발생: {e}")
        return None