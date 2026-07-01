import streamlit as st
import sys
import os
import importlib

# 💡 최상위 경로(C:\Fr_De)를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ==========================================
# 🔄 페이지 전환을 위한 세션 상태(Session State) 초기화
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "dashboard"  # 기본 첫 화면은 대시보드

# ==========================================
# 🎨 메인 상단 헤더 및 화면 전환 버튼
# ==========================================
col_title, col_btn = st.columns([3, 1])

with col_title:
    if st.session_state.page == "dashboard":
        st.title("💳 카드 부정사용 탐지 시스템")
    else:
        st.title("📋 자유 게시판")

with col_btn:
    st.write("") # 버튼 높이 맞춤용 패딩
    if st.session_state.page == "dashboard":
        if st.button("📋 자유 게시판 이동", use_container_width=True):
            st.session_state.page = "board"
            st.rerun()
    else:
        if st.button("💳 탐지 대시보드 이동", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

st.markdown("---")

# ==========================================
# 🔀 importlib.reload를 이용해 화면 강제 렌더링
# ==========================================
if st.session_state.page == "dashboard":
    import app.streamlit_app
    # 💡 이미 로드된 모듈을 강제로 다시 실행하여 화면을 그리게 만듭니다.
    importlib.reload(app.streamlit_app)
    
else:
    import app.board_app
    importlib.reload(app.board_app)