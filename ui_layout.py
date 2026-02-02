import streamlit as st
import engine_ai

# [기존 render_sidebar 함수는 유지]

def render_chatbot(df):
    """R&D 어시스턴트 챗봇 인터페이스"""
    st.divider()
    st.subheader("💬 식품 R&D 어시스턴트 (Context-Aware)")
    st.caption("현재 로드된 기업 정보를 바탕으로 기술적 궁금증을 해결해 드립니다.")

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 채팅 내역 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("식품 소재나 기술에 대해 물어보세요."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("데이터 분석 중..."):
                # 현재 로드된 전체 df를 컨텍스트로 전달
                response = engine_ai.get_chatbot_response(st.session_state.messages, context_df=df)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

def render_results(filtered_df, full_df): # full_df 인자 추가
    if not filtered_df.empty:
        st.subheader(f"📊 기업 정보 조회 (총 {len(filtered_df)}건)")
        
        # 1. 테이블 출력
        display_cols = ['기업이름', '중분류', '소분류', '대표기술', '대표제품']
        st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
        
        st.divider()
        
        # 2. 상세 정보 및 아이디에이션 (기존 로직 유지)
        st.subheader("💡 기업 상세 분석 및 AI 제안")
        target_company = st.selectbox("분석 기업 선택", filtered_df['기업이름'].tolist())
        row = filtered_df[filtered_df['기업이름'] == target_company].iloc[0]
        
        with st.container(border=True):
            st.markdown(f"### 🏢 {target_company}")
            c1, c2 = st.columns(2)
            with c1: st.info(f"**🛠️ 대표기술**\n\n{row['대표기술']}")
            with c2: st.success(f"**📦 대표제품(소재)**\n\n{row['대표제품']}")
            
            site_val = str(row.get('사이트 주소', '-')).strip()
            if site_val and site_val != '-':
                st.link_button("🌐 공식 홈페이지", site_val.split('\n')[0])

        if st.button(f"🚀 {target_company} R&D 리포트 생성"):
            with st.spinner("생성 중..."):
                ideas = engine_ai.get_product_ideation(target_company, row['대표기술'], row['대표제품'])
                st.markdown(ideas)
        
        # 3. 챗봇 실행 (메인 데이터셋 전달)
        render_chatbot(full_df)
