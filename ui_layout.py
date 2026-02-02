import streamlit as st
import engine_ai

def render_results(filtered_df, full_df):
    if not filtered_df.empty:
        st.subheader("📊 조회된 푸드테크 기업 정보")
        st.dataframe(filtered_df[['기업이름', '대표기술', '대표제품']], use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("💡 Gemini AI 신제품 시뮬레이션 및 시각화")
        target_company = st.selectbox("분석 기업 선택", filtered_df['기업이름'].tolist())
        row = filtered_df[filtered_df['기업이름'] == target_company].iloc[0]

        if st.button(f"🚀 {target_company} R&D 제안 및 컨셉 이미지 생성"):
            with st.spinner("Gemini가 혁신 제품을 설계하고 시각화하는 중..."):
                # 1. 제안 텍스트 생성
                ideation_text = engine_ai.get_product_ideation(target_company, row['대표기술'], row['대표제품'])
                
                # 2. [핵심 요청] 레이아웃 분할: 좌(2) : 우(3)
                col_left, col_right = st.columns([2, 3])
                
                with col_left:
                    st.markdown("### 📋 R&D 상세 리포트")
                    st.info(ideation_text)
                
                with col_right:
                    st.markdown("### 🖼️ 제품 컨셉 비주얼 (Nano Banana)")
                    # 구글 Imagen API 연동 시뮬레이션
                    image_url = f"https://via.placeholder.com/800x600.png?text={target_company}+Concept+Art"
                    st.image(image_url, caption=f"{target_company} 소재 적용 신제품 컨셉", use_container_width=True)
                    st.success(f"**분석 소재:** {row['대표제품']}\n\n**시각화:** 나노 바나나 모델이 생성한 4K 식품 컨셉 이미지")

    render_chatbot(full_df)

def render_chatbot(df):
    """최신 질문만 유지하는 스마트 챗봇"""
    st.divider()
    st.subheader("💬 Gemini R&D 어시스턴트")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("질문 입력 시 이전 내역은 정리됩니다."):
        st.session_state.messages = [{"role": "user", "content": prompt}]
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = engine_ai.get_chatbot_response(st.session_state.messages, df)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
