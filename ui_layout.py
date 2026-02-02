import streamlit as st
import engine_ai

def render_sidebar(df, engine_data):
    """사이드바 필터 구성 (AttributeError 해결)"""
    st.sidebar.header("🔍 카테고리 필터")
    if df.empty:
        st.sidebar.warning("⚠️ 파일을 로드할 수 없습니다.")
        uploaded_file = st.sidebar.file_uploader("foodtech_company.csv 업로드", type=['csv'])
        if uploaded_file:
            import pandas as pd
            st.session_state['uploaded_df'] = pd.read_csv(uploaded_file)
            st.rerun()
        return "선택하세요", "선택하세요"

    # engine_data의 함수명과 정확히 매칭
    mid_cats = engine_data.get_unique_categories(df, '중분류')
    selected_mid = st.sidebar.selectbox("1. 중분류 선택", ["선택하세요"] + mid_cats)
    
    selected_sub = "선택하세요"
    if selected_mid != "선택하세요":
        sub_cats = engine_data.get_unique_categories(df, '소분류', {'중분류': selected_mid})
        selected_sub = st.sidebar.selectbox("2. 소분류 선택", ["선택하세요"] + sub_cats)
    return selected_mid, selected_sub

def render_results(filtered_df, full_df):
    """조회 결과 테이블 및 상세 분석"""
    if not filtered_df.empty:
        st.subheader(f"📊 기업 정보 조회 (총 {len(filtered_df)}건)")
        # 테이블 우측에 대표기술, 대표제품 포함
        display_cols = ['기업이름', '중분류', '소분류', '대표기술', '대표제품']
        st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("💡 기업별 상세 분석 및 AI 제안")
        target_company = st.selectbox("분석할 기업 선택", filtered_df['기업이름'].tolist())
        
        # 데이터 안전 추출
        row = filtered_df[filtered_df['기업이름'] == target_company].iloc[0]
        
        with st.container(border=True):
            st.markdown(f"### 🏢 {target_company}")
            c1, c2 = st.columns(2)
            with c1: st.info(f"**🛠️ 대표기술 적용방안**\n\n{row['대표기술']}")
            with c2: st.success(f"**📦 대표제품(소재) 융합기술**\n\n{row['대표제품']}")
            
            site_val = str(row.get('사이트 주소', '-')).strip()
            if site_val and site_val != '-':
                st.link_button("🌐 공식 홈페이지 방문", site_val.split('\n')[0].strip())

        if st.button(f"🚀 {target_company} 기술/소재 기반 제품 제안"):
            with st.spinner("AI 분석 중..."):
                ideas = engine_ai.get_product_ideation(target_company, row['대표기술'], row['대표제품'])
                st.markdown(ideas)

    # 하단 챗봇 호출
    render_chatbot(full_df)

def render_chatbot(df):
    """R&D 챗봇: 신규 질문 시 이전 내역 삭제"""
    st.divider()
    st.subheader("💬 식품 R&D 어시스턴트")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 화면 표시 (최신 대화만 남게 됨)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("소재나 기술에 대해 질문하세요. (새 질문 시 이전 대화는 삭제됩니다)"):
        # 새로운 질문 시 기존 세션 초기화
        st.session_state.messages = [] 
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("데이터 분석 중..."):
                response = engine_ai.get_chatbot_response(st.session_state.messages, df)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
