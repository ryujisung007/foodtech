import streamlit as st
import engine_ai

def render_sidebar(df, engine_data):
    st.sidebar.header("🔍 카테고리 필터")
    
    if df.empty:
        st.sidebar.warning("⚠️ CSV 파일을 로드할 수 없습니다.")
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
        
        # 테이블 형태 조회 결과
        display_cols = ['기업이름', '기업정보', '대표기술', '대표제품', '사이트 주소']
        st.dataframe(
            filtered_df[display_cols],
            use_container_width=True,
            column_config={"사이트 주소": st.column_config.LinkColumn("사이트 바로가기")},
            hide_index=True
        )
        
        st.divider()
        
        # AI 신제품 아이디에이션 섹션
        st.subheader("💡 AI 기반 신제품 R&D 아이디에이션")
        target_company = st.selectbox("분석할 기업을 선택하세요", filtered_df['기업이름'].tolist())
        
        if st.button(f"🚀 {target_company} 기술 기반 제품 창작"):
            row = filtered_df[filtered_df['기업이름'] == target_company].iloc[0]
            with st.spinner(f"{target_company}의 기술과 4대 제품군을 융합 중입니다..."):
                ideas = engine_ai.get_product_ideation(row['기업이름'], row['대표기술'])
                st.markdown("---")
                st.success(f"### 📋 {target_company} 기술 융합 리포트")
                st.markdown(ideas)
    else:
        st.info("카테고리를 선택하면 상세 데이터가 표시됩니다.")
