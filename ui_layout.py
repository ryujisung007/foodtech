import streamlit as st
import engine_ai

def render_sidebar(df, engine_data):
    st.sidebar.header("🔍 카테고리 필터")
    if df.empty:
        st.sidebar.warning("데이터 로드 실패")
        return "선택하세요", "선택하세요"

    mid_cats = engine_data.get_unique_categories(df, '중분류')
    selected_mid = st.sidebar.selectbox("1. 중분류 선택", ["선택하세요"] + mid_cats)
    
    selected_sub = "선택하세요"
    if selected_mid != "선택하세요":
        sub_cats = engine_data.get_unique_categories(df, '소분류', {'중분류': selected_mid})
        selected_sub = st.sidebar.selectbox("2. 소분류 선택", ["선택하세요"] + sub_cats)
    return selected_mid, selected_sub

def render_results(filtered_df, full_df):
    """테이블, 링크, 상세카드, AI 리포트 및 이미지 통합"""
    if not filtered_df.empty:
        # 1. 상단 기업 리스트 테이블 복구
        st.subheader(f"📊 푸드테크 기업 정보 리스트 (총 {len(filtered_df)}건)")
        display_cols = ['기업이름', '중분류', '소분류', '대표기술', '대표제품']
        st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
        
        st.divider()
        
        # 2. 기업 상세 정보 카드 및 홈페이지 링크 복구
        st.subheader("💡 기업별 상세 분석 및 AI 시뮬레이션")
        target_company = st.selectbox("분석할 기업 선택", filtered_df['기업이름'].tolist())
        row = filtered_df[filtered_df['기업이름'] == target_company].iloc[0]
        
        with st.container(border=True):
            st.markdown(f"### 🏢 {target_company}")
            c1, c2 = st.columns(2)
            with c1: st.info(f"**🛠️ 대표기술**\n\n{row['대표기술']}")
            with c2: st.success(f"**📦 대표제품(소재)**\n\n{row['대표제품']}")
            
            # KeyError 방지를 위한 .get 사용
            site_val = str(row.get('사이트 주소', '-')).strip()
            if site_val and site_val != '-':
                clean_url = site_val.split('\n')[0].strip()
                st.link_button("🌐 기업 공식 홈페이지 방문", clean_url)

        # 3. [좌 2 : 우 3] 분할 레이아웃 (리포트 & 나노바나나 그림)
        if st.button(f"🚀 {target_company} 신제품 R&D 제안 및 시각화"):
            with st.spinner("Gemini와 나노바나나가 분석 및 이미지를 생성 중..."):
                ideation_text = engine_ai.get_product_ideation(target_company, row['대표기술'], row['대표제품'])
                
                col_left, col_right = st.columns([2, 3])
                
                with col_left:
                    st.markdown("### 📋 R&D 상세 리포트")
                    st.info(ideation_text)
                
                with col_right:
                    st.markdown("### 🖼️ 신소재 제품 컨셉 아트")
                    # 실제 나노바나나(Imagen) 연동 시뮬레이션
                    # 텍스트가 아닌 실제 이미지가 출력되도록 URL/객체 전달
                    image_url = f"https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=800&q=80"
                    st.image(image_url, 
                             caption=f"{target_company} {row['대표제품']} 적용 컨셉", 
                             use_container_width=True)
                    st.success(f"**적용 소재:** {row['대표제품']}")

    render_chatbot(full_df)

def render_chatbot(df):
    """최신 질문만 유지하는 챗봇"""
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
