import streamlit as st
import engine_ai

def render_results(filtered_df):
    """테이블 출력 -> AI 상세 분석(이미지3개 포함) -> 챗봇 순으로 렌더링"""
    if filtered_df.empty:
        st.warning("조건에 맞는 데이터가 없습니다.")
        return

    # 1. 상단 데이터 테이블 출력
    st.markdown("### 📋 선택된 기업 상세 데이터")
    st.dataframe(filtered_df, use_container_width=True)
    st.divider()

    # 2. 기업별 상세 분석 (좌측 텍스트, 우측 이미지 3개)
    for _, row in filtered_df.iterrows():
        name = row['기업이름']
        tech = str(row.get('대표기술', '정보없음'))
        prod = str(row.get('대표제품', '정보없음'))

        st.header(f"🚀 {name} R&D 시뮬레이션")
        col_text, col_img = st.columns([4, 6])
        
        with col_text:
            st.subheader("💡 신제품 개발 제안")
            with st.spinner(f"{name} 분석 중..."):
                analysis = engine_ai.get_product_ideation(name, tech, prod)
                st.markdown(analysis)
        
        with col_img:
            st.subheader("🎨 추천 시안 (3개)")
            with st.spinner("이미지 생성 중..."):
                imgs = engine_ai.generate_nano_banana_images(tech, prod)
                if imgs:
                    for idx, img in enumerate(imgs):
                        st.image(img, caption=f"Concept Art {idx+1}", use_container_width=True)
                else:
                    st.info("🎨 이미지 생성 엔진을 로드하고 있습니다.")
        st.divider()

    # 3. 하단 챗봇 복구
    st.markdown("### 💬 R&D 전문가 상담 챗봇")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("신제품 개발에 대해 더 질문해 보세요!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response = engine_ai.get_product_ideation("전문상담", "질의응답", prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
