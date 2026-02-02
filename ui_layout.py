import streamlit as st
import engine_ai

def render_results(filtered_df):
    """테이블 -> AI 분석(이미지 포함) -> 챗봇 순으로 출력"""
    if filtered_df.empty:
        st.warning("조건에 맞는 데이터가 없습니다.")
        return

    # 1. 상단 데이터 테이블
    st.markdown("### 📋 분석 대상 기업 데이터")
    st.dataframe(filtered_df, use_container_width=True)
    st.divider()

    # 2. 상세 시뮬레이션
    for _, row in filtered_df.iterrows():
        name = row['기업이름']
        tech = str(row.get('대표기술', '정보없음'))
        prod = str(row.get('대표제품', '정보없음'))

        st.header(f"🚀 {name} R&D 시뮬레이션")
        col_text, col_img = st.columns([4, 6])
        
        with col_text:
            st.subheader("💡 신제품 개발 제안")
            with st.spinner("AI 분석 엔진 가동 중..."):
                analysis = engine_ai.get_product_ideation(name, tech, prod)
                st.markdown(analysis)
        
        with col_img:
            st.subheader("🎨 추천 시안 (3개)")
            with st.spinner("나노 바나나가 생성 중..."):
                imgs = engine_ai.generate_nano_banana_images(tech, prod)
                if imgs:
                    for idx, img in enumerate(imgs):
                        st.image(img, caption=f"Concept {idx+1}", use_container_width=True)
                else:
                    st.info("🎨 이미지 생성 엔진을 로드 중입니다.")
        st.divider()

    # 3. 챗봇 인터페이스 (하단 고정)
    st.markdown("### 💬 R&D 전문가 챗봇 상담")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("신제품 개발에 대해 더 물어보세요!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            # 챗봇 응답 시에도 안정적인 모델 호출 사용
            response = engine_ai.get_product_ideation("전문상담", "질의", prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
