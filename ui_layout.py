import streamlit as st
import engine_ai

def render_results(filtered_df):
    """결과 화면: 테이블 출력 + AI 분석 + 이미지 3개"""
    if filtered_df.empty:
        st.warning("조회된 데이터가 없습니다.")
        return

    # 1. 원본 데이터 테이블 출력 (복구된 기능)
    st.markdown("### 📋 선택 기업 상세 정보")
    st.dataframe(filtered_df, use_container_width=True)
    st.divider()

    # 2. 기업별 상세 분석 (좌측 텍스트, 우측 이미지 3개)
    for _, row in filtered_df.iterrows():
        name = row['기업이름']
        tech = str(row.get('대표기술', '정보없음'))
        prod = str(row.get('대표제품', '정보없음'))

        st.header(f"🔬 {name} R&D 시뮬레이션")
        col_left, col_right = st.columns([4, 6])
        
        with col_left:
            st.subheader("💡 신제품 개발 제안")
            with st.spinner("AI가 분석 중..."):
                analysis = engine_ai.get_product_ideation(name, tech, prod)
                st.markdown(analysis)
        
        with col_right:
            st.subheader("🎨 추천 시안 (3개)")
            with st.spinner("이미지 생성 중..."):
                imgs = engine_ai.generate_nano_banana_images(tech, prod)
                if imgs:
                    for i, img in enumerate(imgs):
                        st.image(img, caption=f"시안 {i+1}", use_container_width=True)
                else:
                    st.info("이미지 생성 기능을 준비 중입니다.")
        st.divider()
