import streamlit as st
import engine_ai

# [render_sidebar 및 기타 함수는 이전과 동일하게 유지]

def render_results(filtered_df, full_df):
    if not filtered_df.empty:
        st.subheader(f"📊 기업 정보 조회")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        st.subheader("💡 Gemini AI R&D 시뮬레이션")
        target_company = st.selectbox("기업 선택", filtered_df['기업이름'].tolist())
        row = filtered_df[filtered_df['기업이름'] == target_company].iloc[0]
        
        # 정보 출력
        with st.container(border=True):
            st.markdown(f"### 🏢 {target_company}")
            c1, c2 = st.columns(2)
            c1.info(f"**🛠️ 기술:** {row['대표기술']}")
            c2.success(f"**📦 소재:** {row['대표제품']}")

        # 제안 및 이미지 생성 버튼
        if st.button(f"🚀 {target_company} 신제품 제안 및 시각화"):
            with st.spinner("Gemini가 제품을 설계하고 이미지를 그리는 중..."):
                # 1. 텍스트 제안 생성
                ideation_text = engine_ai.get_product_ideation(target_company, row['대표기술'], row['대표제품'])
                
                # 2. 화면 레이아웃 분할 (좌측: 설명 / 우측: 그림)
                col_text, col_img = st.columns([2, 3])
                
                with col_text:
                    st.markdown("### 📋 R&D 리포트")
                    st.markdown(ideation_text)
                
                with col_img:
                    st.markdown("### 🖼️ 시각적 컨셉 (AI 생성)")
                    # 4대 카테고리 중 대표 카테고리 하나를 이미지화
                    img_data = engine_ai.generate_concept_image(f"Innovative food product using {row['대표제품']}")
                    if img_data:
                        st.image(img_data, use_container_width=True, caption=f"{target_company} 컨셉 이미지")
                    else:
                        st.warning("이미지 모델 접근 권한을 확인하세요. (API 할당량 또는 Imagen 권한)")
                        # 대체 이미지 또는 구조도 표시 가능
                        st.info("💡 이미지 생성 프롬프트 예시: " + f"High-end {row['대표제품']} dessert concept.")

    # 챗봇 호출
    render_chatbot(full_df)
