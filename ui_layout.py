import streamlit as st
import engine_ai

def render_results(filtered_df, full_df):
    """결과 화면 렌더링: 좌측 설명 / 우측 이미지 3개 배치"""
    if filtered_df.empty:
        st.warning("분석할 데이터가 없습니다.")
        return

    for index, row in filtered_df.iterrows():
        target_company = row['회사명']
        st.subheader(f"🏢 {target_company} 분석 및 제안")
        
        # 레이아웃 분할: 좌측 4(설명), 우측 6(이미지들)
        col_text, col_img = st.columns([4, 6])
        
        with col_text:
            st.markdown("### 💡 제품 및 기술 제안")
            # 에러 발생 지점 수정: engine_ai의 함수 호출
            with st.spinner("제미나이가 아이디어를 짜는 중..."):
                ideation_text = engine_ai.get_product_ideation(target_company, row['대표기술'], row['대표제품'])
                st.write(ideation_text)
        
        with col_img:
            st.markdown("### 🎨 AI 추천 이미지 (by Nano Banana)")
            with st.spinner("3개의 이미지를 생성 중..."):
                # 이미지 3개 생성 요청
                generated_images = engine_ai.generate_nano_banana_images(row['대표기술'], row['대표제품'], count=3)
                
                if generated_images:
                    # 3개 이미지를 세로 혹은 그리드로 배치 (여기서는 세로 배치 예시)
                    for i, img in enumerate(generated_images):
                        st.image(img, caption=f"추천 시안 {i+1}", use_container_width=True)
                else:
                    st.info("이미지를 생성할 수 없거나 API 설정이 필요합니다.")
        st.divider()
