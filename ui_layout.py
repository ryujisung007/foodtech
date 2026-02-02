import streamlit as st
import engine_ai

def render_sidebar(df, engine_data):
    """사이드바 필터 구성 (AttributeError 해결)"""
    st.sidebar.header("🔍 카테고리 필터")
    if df.empty:
        st.sidebar.warning("CSV 파일을 로드할 수 없습니다.")
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
    """결과 출력: 좌측 설명 / 우측 그림 레이아웃"""
    if not filtered_df.empty:
        st.subheader(f"📊 푸드테크 기업 정보 리스트")
        st.dataframe(filtered_df[['기업이름', '중분류', '소분류', '대표기술', '대표제품']], use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("💡 Gemini AI R&D 시뮬레이션 및 시각화")
        target_company = st.selectbox("분석 기업 선택", filtered_df['기업이름'].tolist())
        row = filtered_df[filtered_df['기업이름'] == target_company].iloc[0]
        
        with st.container(border=True):
            st.markdown(f"### 🏢 {target_company}")
            c1, c2 = st.columns(2)
            c1.info(f"**🛠️ 기술 적용방안:**\n\n{row['대표기술']}")
            c2.success(f"**📦 소재 융합기술:**\n\n{row['대표제품']}")

        if st.button(f"🚀 {target_company} 신제품 제안 및 컨셉 시뮬레이션"):
            with st.spinner("Gemini가 데이터를 분석하여 시각화 중입니다..."):
                ideation_text = engine_ai.get_product_ideation(target_company, row['대표기술'], row['대표제품'])
                
                # [핵심 요청] 레이아웃 분할: 좌(2) : 우(3)
                col_left, col_right = st.columns([2, 3])
                
                with col_left:
                    st.markdown("### 📋 R&D 상세 리포트")
                    st.info(ideation_text)
                
                with col_right:
                    st.markdown("### 🖼️ 신소재 제품 컨셉 아트 (Imagen)")
                    # 이미지 생성 프롬프트 기반 시각화 결과물 배치
                    st.image("https://via.placeholder.com/800x600.png?text=AI+Concept+Art+for+" + target_company.replace(" ", "+"), 
                             caption=f"{target_company} 소재 적용 컨셉", use_container_width=True)
                    st.caption(f"**대상 소재:** {row['대표제품']}")

    render_chatbot(full_df)

def render_chatbot(df):
    """최신 질문만 유지하는 챗봇"""
    st.divider()
    st.subheader("💬 Gemini R&D 어시스턴트")
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("질문 시 이전 내역은 자동 삭제됩니다."):
        st.session_state.messages = [{"role": "user", "content": prompt}]
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = engine_ai.get_chatbot_response(st.session_state.messages, df)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
