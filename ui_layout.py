import streamlit as st
import engine_ai

def render_sidebar(df, engine_data):
    st.sidebar.header("🔍 카테고리 필터")
    if df.empty:
        st.sidebar.warning("데이터 로드 실패")
        return "선택하세요", "선택하세요"

    # engine_data 함수명 일치 확인 필수
    mid_cats = engine_data.get_unique_categories(df, '중분류')
    selected_mid = st.sidebar.selectbox("1. 중분류 선택", ["선택하세요"] + mid_cats)
    
    selected_sub = "선택하세요"
    if selected_mid != "선택하세요":
        sub_cats = engine_data.get_unique_categories(df, '소분류', {'중분류': selected_mid})
        selected_sub = st.sidebar.selectbox("2. 소분류 선택", ["선택하세요"] + sub_cats)
    return selected_mid, selected_sub

def render_results(filtered_df, full_df):
    """좌측 설명 / 우측 그림 레이아웃"""
    if not filtered_df.empty:
        st.subheader("📊 푸드테크 기업 정보")
        st.dataframe(filtered_df[['기업이름', '대표기술', '대표제품']], use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("💡 Gemini AI R&D 시뮬레이션")
        target_company = st.selectbox("분석 기업 선택", filtered_df['기업이름'].tolist())
        row = filtered_df[filtered_df['기업이름'] == target_company].iloc[0]
        
        if st.button(f"🚀 {target_company} 신제품 제안 및 시각화"):
            with st.spinner("Gemini가 데이터를 분석하고 이미지를 생성 중..."):
                ideation_text = engine_ai.get_product_ideation(target_company, row['대표기술'], row['대표제품'])
                
                # [좌 2 : 우 3] 레이아웃 분할
                col_left, col_right = st.columns([2, 3])
                
                with col_left:
                    st.markdown("### 📋 R&D 상세 리포트")
                    st.info(ideation_text)
                
                with col_right:
                    st.markdown("### 🖼️ 신소재 제품 컨셉 아트")
                    # 이미지 생성 컨셉 시뮬레이션
                    image_url = f"https://via.placeholder.com/800x600.png?text={target_company}+Food+Concept"
                    st.image(image_url, caption=f"{target_company} {row['대표제품']} 적용 컨셉", use_container_width=True)
                    st.success(f"**적용 소재:** {row['대표제품']}")

    render_chatbot(full_df)

def render_chatbot(df):
    st.divider()
    st.subheader("💬 Gemini R&D 어시스턴트")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("새 질문 시 이전 대화는 삭제됩니다."):
        st.session_state.messages = [{"role": "user", "content": prompt}]
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = engine_ai.get_chatbot_response(st.session_state.messages, df)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
