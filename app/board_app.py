import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# =========================
# 🗄️ 데이터베이스 초기화 함수
# =========================
def init_db():
    conn = sqlite3.connect("board.db")
    cursor = conn.cursor()
    # 게시글 테이블 생성 (없으면 생성)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# 데이터베이스 연결 및 쿼리 실행 헬퍼 함수
def run_query(query, params=(), is_select=False):
    conn = sqlite3.connect("board.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    if is_select:
        data = cursor.fetchall()
        conn.close()
        return data
    conn.commit()
    conn.close()

# 데이터베이스 초기화 실행
init_db()

# =========================
# 🎨 사이드바 메뉴 구성
# =========================
st.sidebar.title("📌 게시판 메뉴")
menu = st.sidebar.radio("원하는 작업을 선택하세요", ["📋 글 목록 보기", "✍️ 새 글 작성하기", "❌ 글 삭제하기"])

# =========================
# 📋 1. 글 목록 보기 기능
# =========================
if menu == "📋 글 목록 보기":
    st.title("")
    
    # DB에서 전체 글 가져오기
    data = run_query("SELECT id, title, author, created_at FROM posts ORDER BY id DESC", is_select=True)
    
    if not data:
        st.info("아직 등록된 게시글이 없습니다. 첫 글을 작성해 보세요!")
    else:
        # 데이터프레임으로 깔끔하게 변환하여 목록 표시
        df = pd.DataFrame(data, columns=["번호", "제목", "작성자", "작성일"])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("🔍 본문 읽기")
        
        # 읽고 싶은 글 선택 콤보박스
        post_titles = [f"{row[0]}. {row[1]} (by {row[2]})" for row in data]
        selected_post = st.selectbox("상세 내용을 볼 게시글을 선택하세요", post_titles)
        
        if selected_post:
            post_id = int(selected_post.split(".")[0])
            post_detail = run_query("SELECT title, author, content, created_at FROM posts WHERE id = ?", (post_id,), is_select=True)
            
            if post_detail:
                title, author, content, created_at = post_detail[0]
                st.markdown(f"### `{title}`")
                st.caption(f"✍️ 작성자: **{author}** | 📅 작성일: {created_at}")
                st.info(content)

# =========================
# ✍️ 2. 새 글 작성하기 기능
# =========================
elif menu == "✍️ 새 글 작성하기":
    st.title("✍️ 새 글 작성하기")
    
    with st.form("board_form", clear_on_submit=True):
        title = st.text_input("제목", placeholder="제목을 입력하세요.")
        author = st.text_input("작성자", placeholder="닉네임을 입력하세요.")
        content = st.text_area("내용", placeholder="내용을 입력하세요.", height=200)
        submit_button = st.form_submit_button("🚀 게시하기")
        
        if submit_button:
            if title and author and content:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                run_query(
                    "INSERT INTO posts (title, author, content, created_at) VALUES (?, ?, ?, ?)",
                    (title, author, content, now)
                )
                st.success("🎉 글이 성공적으로 등록되었습니다! '글 목록 보기'에서 확인하세요.")
            else:
                st.error("❌ 제목, 작성자, 내용을 모두 입력해 주세요.")

# =========================
# ❌ 3. 글 삭제하기 기능
# =========================
elif menu == "❌ 글 삭제하기":
    st.title("❌ 게시글 삭제")
    
    data = run_query("SELECT id, title, author FROM posts ORDER BY id DESC", is_select=True)
    
    if not data:
        st.info("삭제할 게시글이 없습니다.")
    else:
        post_titles = [f"{row[0]}. {row[1]} (by {row[2]})" for row in data]
        selected_post = st.selectbox("삭제할 게시글을 선택하세요", post_titles)
        
        if st.button("⚠️ 정말로 삭제하시겠습니까?", type="primary"):
            post_id = int(selected_post.split(".")[0])
            run_query("DELETE FROM posts WHERE id = ?", (post_id,))
            st.success("🗑️ 게시글이 삭제되었습니다.")
            st.rerun()