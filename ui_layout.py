import streamlit as st
import engine_ai

def render_sidebar(df, engine_data):
    st.sidebar.header("🔍 검색 필터")
    if df.empty:
        st.sidebar.warning("⚠️ 파일을 로드할 수 없습니다.")
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
        st.subheader(f"✅ 조회 결과 ({len(filtered_df)}개 기업)")
        
        # 1. 테이블 출력
        display_cols = ['기업이름', '기업정보', '대표기술', '대표제품', '사이트 주소']
        st.dataframe(
            filtered_df[display_cols],
            use_container_width=True,
            column_config={"사이트 주소": st.column_config.LinkColumn()},
            hide_index=True
        )
        
        st.divider()
        
        # 2. 아이디에이션 섹션
        st.subheader("💡 AI 제품 아이디에이션 (기술 기반)")
        target_company = st.selectbox("아이디어를 생성할 기업을 선택하세요", filtered_df['기업이름'].tolist())
        
        if st.button(f"'{target_company}' 기술로 제품 제안받기"):
            row = filtered_df[filtered_df['기업이름'] == target_company].iloc[0]
            with st.spinner("AI가 식품 공학적 관점에서 아이디어를 짜고 있습니다..."):
                ideas = engine_ai.get_product_ideation(row['기업이름'], row['대표기술'])
                st.info(f"**[{target_company}] R&D 제안**")
                st.write(ideas)
    else:
        st.info("데이터가 없습니다.")
