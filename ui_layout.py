import streamlit as st
import engine_ai

# [기존 render_sidebar 함수는 동일하게 유지]

def render_chatbot(df):
    """R&D 어시스턴트 챗봇 (신규 질문 시 이전 내용 삭제 버전)"""
    st.divider()
    st.subheader("💬 식품 R&D 어시스턴트")
    st.caption("새로운 질문을 입력하면 이전 대화 내역은 자동으로 정리됩니다.")

    # 1. 세션 상태 초기화 (대화 내역을 담는 리스트)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 2. 현재 대화 내역 표시 (초기화 후에는 1개 세트만 표시됨)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 3. 사용자 입력 처리
    if prompt := st.chat_input("소재나 기술, 배합비에 대해 질문하세요."):
        # [핵심 수정] 새로운 질문이 들어오면 기존 대화 내역을 비웁니다.
        st.session_state.messages = [] 
        
        # 사용자 메시지 추가 및 출력
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답 생성 및 출력
        with st.chat_message("assistant"):
            with st.spinner("데이터 기반 답변 생성 중..."):
                response = engine_ai.get_chatbot_response(st.session_state.messages, df)
                st.markdown(response)
                # AI 메시지 세션에 저장 (최신 1건 유지)
                st.session_state.messages.append({"role": "assistant", "content": response})
