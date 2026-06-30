import streamlit as st
import numpy as np
import sys
import os

# 💡 src 폴더를 참조하기 위해 경로를 추가합니다.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import load_scaler, load_autoencoder_model

# =========================
# 🎛️ 사이버 보안 대시보드형 전면 리디자인 CSS
# =========================
st.markdown("""
    <style>
        /* 1. 전체 앱 배경을 어두운 미래형 네이비로 변경 */
        .stApp {
            background-color: #0b0f19 !important;
            color: #e2e8f0 !important;
        }
        
        /* 2. 상단 헤더 및 텍스트 컬러 변경 */
        h1 {
            color: #38bdf8 !important; /* 사이언 블루 */
            font-family: 'Pretendard', 'Malgun Gothic', sans-serif;
            font-weight: 800;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
            margin-bottom: 5px !important;
        }
        div[data-testid="stMarkdownContainer"] p {
            color: #94a3b8 !important;
        }
        
        /* 3. 입력 영역을 하나의 멋진 '보안 카드' 형태로 묶기 */
        div[data-testid="stVerticalBlock"] > div {
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 12px;
            padding: 5px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        }
        
        /* 4. 입력창 라벨 및 내부 스타일 커스텀 */
        label {
            color: #38bdf8 !important; /* 라벨을 하늘색으로 투명하게 포인트를 줌 */
            font-weight: 600 !important;
            font-size: 14px !important;
        }
        input {
            background-color: #1f2937 !important;
            color: #ffffff !important;
            border: 1px solid #374151 !important;
            border-radius: 6px !important;
        }
        
        /* 5. 🔍 사기 여부 검사 버튼의 압도적인 변신 */
        div.stButton > button:first-child {
            background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            font-size: 18px !important;
            font-weight: bold !important;
            height: 54px !important;
            width: 100% !important;
            box-shadow: 0 0 15px rgba(2, 132, 199, 0.4) !important;
            transition: all 0.25s ease-in-out !important;
            margin-top: 15px;
        }
        
        div.stButton > button:first-child:hover {
            background: linear-gradient(90deg, #38bdf8 0%, #0284c7 100%) !important;
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.6) !important;
            transform: translateY(-2px);
        }
        
        /* 6. 결과 메시지 박스 커스텀 */
        div.stAlert {
            background-color: #1e1b4b !important; /* 사기 의심시 딥 퍼플/레드 톤 */
            border: 1px solid #4338ca !important;
            border-radius: 8px !important;
        }
        
        /* 7. 구분선(hr) 색상 세련되게 변경 */
        hr {
            border-color: #1f2937 !important;
        }
    </style>
""", unsafe_allow_html=True)

# =========================
# 🎯 기본 화면 및 모델 로드
# =========================
st.title("💳 카드 부정사용 탐지 시스템 (Fraud Detection)")

# 💡 모델 파일명을 실제 유저님의 파일명인 autoencoder.h5로 정상 수정했습니다!
try:
    scaler = load_scaler("models/scaler.pkl")
    model = load_autoencoder_model("models/autoencoder.h5")
except Exception as e:
    scaler = None
    model = None

st.markdown("---")

# =========================
# 📥 사용자 입력
# =========================
st.header("📥 거래 정보 입력")
amount = st.number_input("거래 금액", min_value=0.0, value=1000.0)
old_balance = st.number_input("기존 잔액", min_value=0.0, value=5000.0)
new_balance = st.number_input("변경 후 잔액", min_value=0.0, value=4000.0)

old_balance_dest = st.number_input("수신자 기존 잔액", min_value=0.0, value=0.0)
new_balance_dest = st.number_input("수신자 변경 후 잔액", min_value=0.0, value=0.0)

transaction_type = st.selectbox("거래 유형", ["PAYMENT(결제, 지불)", "TRANSFER(이체, 송금)", "CASH_OUT(현금 인출, 출금)", "DEBIT(출금, 계좌 인출, 직불)"])

st.markdown("---")

# =========================
# 🔍 예측 버튼 (진짜 AI 연동)
# =========================
if st.button("🔍 사기 여부 검사"):
    if model is not None and scaler is not None:
        input_data = np.array([[amount, old_balance, new_balance, old_balance_dest, new_balance_dest]])
        input_scaled = scaler.transform(input_data)
        
        reconstructed = model.predict(input_scaled)
        score = np.mean(np.power(input_scaled - reconstructed, 2))

        st.subheader("📊 분석 결과")
        st.write(f"거래 유형: {transaction_type}")
        st.write(f"재구성 손실 점수 (Anomaly Score): {score:.4f}")

        threshold = 2.0 
        
        progress = min(score / (threshold * 2), 1.0)
        st.progress(progress)

        if score > threshold:
            st.error("🚨 사기 거래 의심 (Fraud Detected)")
            st.write("→ 오토인코더가 비정상적인 복원 에러를 감지했습니다.")
        else:
            st.success("✅ 정상 거래")
            st.write("→ 정상 범위 내의 거래 패턴입니다.")
    else:
        st.error("❌ 모델 또는 스케일러를 불러오지 못했습니다. models/ 폴더 내 파일 경로를 확인해 주세요.")