import streamlit as st
import engine_ai

def render_sidebar(df, engine_data):
    st.sidebar.header("🔍 카테고리 필터")
    if df.empty:
        st.sidebar.warning("⚠️ 파일을 찾을 수 없습니다.")
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
        
        # [수정] 대표기술, 대표제품 컬럼을 우측에 추가하여 테이블 구성
        display_cols = ['기업이름', '중분류', '소분류', '대표기술', '대표제품']
        st.dataframe(
            filtered_df[display_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "대표기술": st.column_config.TextColumn("대표기술", width="medium"),
                "대표제품": st.column_config.TextColumn("대표제품", width="medium")
            }
        )
        
        st.divider()
        
        st.subheader("💡 기업별 상세 분석 및 AI 제안")
        company_list = filtered_df['기업이름'].tolist()
        target_company = st.selectbox("분석할 기업을 선택하세요", company_list)
        
        # 데이터 안전 추출 (TypeError 방지)
        selected_row = filtered_df[filtered_df['기업이름'] == target_company].iloc[0]
        tech_val = selected_row['대표기술']
        prod_val = selected_row['대표제품']
        site_val = str(selected_row.get('사이트 주소', '-')).strip()

        with st.container(border=True):
            st.markdown(f"### 🏢 {target_company}")
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**🛠️ 대표기술**\n\n{tech_val}")
            with c2:
                st.success(f"**📦 대표제품(소재)**\n\n{prod_val}")
            
            # [유지] 홈페이지 연결 버튼 추가
            if site_val and site_val != '-':
                clean_url = site_val.split('\n')[0].strip()
                st.link_button("🌐 기업 공식 홈페이지 방문", clean_url, use_container_width=True)

        if st.button(f"🚀 {target_company} 기술 및 소재 기반 신제품 제안"):
            with st.spinner("AI가 분석 중입니다..."):
                ideas = engine_ai.get_product_ideation(target_company, tech_val, prod_val)
                st.markdown("---")
                st.markdown(f"### 📋 {target_company} R&D 아이디어 리포트")
                st.markdown(ideas)
    else:
        st.info("카테고리를 선택해 주세요.")
