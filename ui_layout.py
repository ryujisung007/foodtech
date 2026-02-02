import streamlit as st
import engine_ai

def render_results(filtered_df):
    """데이터 테이블과 AI 시뮬레이션을 안정적으로 출력"""
    if filtered_df.empty:
        st.warning("데이터가 없습니다.")
        return

    # 상단 데이터 테이블
    st.markdown("### 📋 기업 데이터 리스트")
    st.dataframe(filtered_df, use_container_width=True)
    st.divider()

    for _, row in filtered_df.iterrows():
        # 원본 CSV의 정확한 헤더인 '기업이름' 사용
        name = row['기업이름']
        tech = str(row.get('대표기술', '정보없음'))
        prod = str(row.get('대표제품', '정보없음'))

        st.header(f"🔬 {name} R&D 시뮬레이션")
        col_left, col_right = st.columns([4, 6])
        
        with col_left:
            st.subheader("💡 신제품 개발 제안")
            with st.spinner("전문 AI가 분석 중..."):
                analysis = engine_ai.get_product_ideation(name, tech, prod)
                st.markdown(analysis)
        
        with col_right:
            st.subheader("🎨 추천 시안 (3개)")
            with st.spinner("나노 바나나가 생성 중..."):
                imgs = engine_ai.generate_nano_banana_images(tech, prod)
                if imgs:
                    for i, img in enumerate(imgs):
                        st.image(img, caption=f"시안 {i+1}", use_container_width=True)
                else:
                    st.info("이미지 생성 기능을 불러오지 못했습니다. API 설정을 확인해 주세요.")
        st.divider()

    # 결과 하단에 챗봇 인터페이스가 항상 나타나도록 배치 (복구됨)
    st.markdown("### 💬 R&D 어시스턴트 챗봇")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("신제품 개발에 대해 더 궁금한 점을 물어보세요!"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 챗봇 응답 로직 (Gemini 활용)
        with st.chat_message("assistant"):
            response = engine_ai.get_product_ideation("챗봇상담", "상담", prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
