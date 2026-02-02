import streamlit as st
import engine_ai

def render_sidebar(df, engine_data):
    st.sidebar.header("🔍 카테고리 필터")
    
    if df.empty:
        st.sidebar.warning("⚠️ 데이터를 로드할 수 없습니다.")
        uploaded_file = st.sidebar.file_uploader("foodtech_company.csv 업로드", type=['csv'])
        if uploaded_file:
            import pandas as pd
            st.session_state['uploaded_df'] = pd.read_csv(uploaded_file)
            st.rerun()
        return "선택하세요", "선택하세요"

    mid_cats = engine_data.get_unique_categories(df, '중분류')
    selected_mid = st.sidebar.selectbox("1. 중분류 선택", ["선택하세요"] + mid_cats)
    
    selected_sub = "선택하세요"
    if selected_mid != "선택하세요":
        sub_cats = engine_data.get_unique_categories(df, '소분류', {'중분류': selected_mid})
        selected_sub = st.sidebar.selectbox("2. 소분류 선택", ["선택하세요"] + sub_cats)
        
    return selected_mid, selected_sub

def render_results(filtered_df):
    if not filtered_df.empty:
        st.subheader(f"📊 기업 정보 조회 (총 {len(filtered_df)}건)")
        
        # 1. 테이블 출력 (사이트 주소 제외하여 가독성 증대)
        display_cols = ['기업이름', '기업정보', '대표기술', '대표제품']
        st.dataframe(
            filtered_df[display_cols],
            use_container_width=True,
            hide_index=True
        )
        
        st.divider()
        
        # 2. 기업 선택 상세 정보 및 사이트 주소 출력 칸
        st.subheader("💡 기업별 상세 분석 및 AI 제안")
        target_company = st.selectbox("분석할 기업을 선택하세요", filtered_df['기업이름'].tolist())
        
        # 선택된 기업 데이터 추출
        row = filtered_df[filtered_df['기업이름'] == target_company].iloc[0]
        
        # 사이트 주소 및 기본 정보 카드형 출력
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**🏢 기업명:** {target_company}")
                st.markdown(f"**🛠️ 대표기술:** {row['대표기술']}")
            with col2:
                # 사이트 주소가 있는 경우 버튼 활성화
                site_url = str(row['사이트 주소']).strip()
                if site_url and site_url != '-':
                    # 줄바꿈으로 여러 URL이 있는 경우 첫 번째 URL 추출
                    clean_url = site_url.split('\n')[0].strip()
                    st.link_button("🌐 공식 사이트 방문", clean_url)
                else:
                    st.write("사이트 정보 없음")

        # 3. AI 아이디에이션 버튼
        if st.button(f"🚀 {target_company} 기술 기반 신제품 제안받기"):
            with st.spinner(f"AI가 {target_company}의 기술을 분석 중입니다..."):
                ideas = engine_ai.get_product_ideation(row['기업이름'], row['대표기술'])
                st.markdown("---")
                st.success(f"### 📋 {target_company} R&D 아이디어 리포트")
                st.markdown(ideas)
    else:
        st.info("카테고리를 선택하면 상세 데이터가 표시됩니다.")
