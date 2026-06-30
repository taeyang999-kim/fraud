import streamlit as st
import numpy as np

# =========================
# 🎯 기본 화면
# =========================
st.title("💳 카드 부정사용 탐지 시스템 (Fraud Detection)")
st.write("Autoencoder 기반 이상탐지 데모 시스템입니다.")

st.markdown("---")

# =========================
# 📥 사용자 입력
# =========================
st.header("📥 거래 정보 입력")

amount = st.number_input("거래 금액", min_value=0.0, value=1000.0)
old_balance = st.number_input("기존 잔액", min_value=0.0, value=5000.0)
new_balance = st.number_input("변경 후 잔액", min_value=0.0, value=4000.0)

transaction_type = st.selectbox(
    "거래 유형",
    ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT"]
)

st.markdown("---")

# =========================
# 🤖 (임시) AI 모델 로직
# =========================
def fake_autoencoder_error(amount, old, new):
    """
    👉 실제 모델 대신 임시 이상탐지 점수 계산
    """
    balance_diff = abs(old - new)
    score = (amount + balance_diff) / (old + 1)

    return score


# =========================
# 🔍 예측 버튼
# =========================
if st.button("🔍 사기 여부 검사"):

    score = fake_autoencoder_error(amount, old_balance, new_balance)

    st.subheader("📊 분석 결과")

    st.write(f"거래 유형: {transaction_type}")
    st.write(f"이상 점수 (Fraud Score): {score:.3f}")

    # =========================
    # 🚨 판정 기준
    # =========================
    threshold = 1.0

    progress = min(score / 2, 1.0)
    st.progress(progress)

    if score > threshold:
        st.error("🚨 사기 거래 의심 (Fraud Detected)")
        st.write("→ 시스템이 비정상 패턴을 감지했습니다.")
    else:
        st.success("✅ 정상 거래")
        st.write("→ 정상적인 거래 패턴입니다.")

st.markdown("---")

# =========================
# 📌 설명 영역 (발표용)
# =========================
st.subheader("📌 시스템 설명")
st.write("""
이 시스템은 금융 거래 데이터를 기반으로  
비정상 거래를 탐지하는 이상탐지 모델입니다.

- 입력: 거래 금액, 잔액 변화, 거래 유형
- 출력: 정상 / 사기 판정
- 방식: 이상 점수 기반 탐지 (추후 Autoencoder 적용)
""")

st.markdown("---")

st.caption("© Fraud Detection AI Project - Streamlit Demo")