import streamlit as st
import engine_ai

def render_results(filtered_df):
    """좌측 설명, 우측 3개 이미지 레이아웃 렌더링"""
    if filtered_df.empty:
        st.warning("데이터가 없습니다.")
        return

    for _, row in filtered_df.iterrows():
        # 원본 DB 헤더 '기업이름' 사용
        name = row['기업이름']
        tech = row.get('대표기술', '일반 기술')
        prod = row.get('대표제품', '일반 제품')

        st.subheader(f"🏢 {name} R&D 분석 결과")
        col_text, col_img = st.columns([4, 6])
        
        with col_text:
            st.info("💡 신제품 제안")
            with st.spinner("AI 분석 중..."):
                ideation = engine_ai.get_product_ideation(name, tech, prod)
                st.markdown(ideation)
        
        with col_img:
            st.success("🎨 추천 이미지 시안 (3개)")
            with st.spinner("나노 바나나가 생성 중..."):
                imgs = engine_ai.generate_nano_banana_images(tech, prod)
                if imgs:
                    for i, img in enumerate(imgs):
                        st.image(img, caption=f"시안 {i+1}", use_container_width=True)
                else:
                    st.info("이미지 생성 API를 확인해주세요.")
        st.divider()
