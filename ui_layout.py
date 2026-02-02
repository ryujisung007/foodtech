import streamlit as st
import engine_ai

def render_results(filtered_df, full_df):
    """결과 화면: 좌측 설명 / 우측 이미지 3개 리스트"""
    if filtered_df.empty:
        st.warning("데이터가 존재하지 않습니다.")
        return

    for _, row in filtered_df.iterrows():
        st.header(f"📊 {row['회사명']} R&D 시뮬레이션")
        
        col_left, col_right = st.columns([4, 6])
        
        with col_left:
            st.subheader("💡 신제품 개발 제안")
            with st.spinner("AI 분석 중..."):
                analysis = engine_ai.get_product_ideation(
                    row['회사명'], row['대표기술'], row['대표제품']
                )
                st.markdown(analysis)
        
        with col_right:
            st.subheader("🎨 추천 디자인 시안 (3개)")
            with st.spinner("나노 바나나가 그림을 그리는 중..."):
                images = engine_ai.generate_nano_banana_images(
                    row['대표기술'], row['대표제품']
                )
                
                if images:
                    for idx, img in enumerate(images):
                        st.image(img, caption=f"시안 {idx+1}", use_container_width=True)
                else:
                    st.info("이미지 생성 기능을 준비 중이거나 API 할당량이 초과되었습니다.")
        st.divider()
