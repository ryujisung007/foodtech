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
        
        # [수정] 테이블에서는 '사이트 주소'를 제외하여 깔끔하게 표시
        display_cols = ['기업이름', '기업정보', '대표기술', '대표제품']
        st.dataframe(
            filtered_df[display_cols],
            use_container_width=True,
            hide_index=True
        )
        
        st.divider()
        
        # [개선] 기업 선택 시 상세 정보 및 사이트 주소 출력
        st.subheader("💡 기업별 상세 분석 및 AI 제품 제안")
        target_company = st.selectbox("분석할 기업을 선택하세요", filtered_df['기업이름'].tolist())
        
        # 선택된 기업의 행 데이터 가져오기
        row = filtered_df[filtered_df['기업이름'] == target_company].iloc[0]
        
        # [요청 반영] 사이트 주소 출력 칸
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**🏢 {target_company}** | {row['대표제품']}")
            with col2:
                # 사이트 주소가 존재할 경우에만 버튼/링크 표시
                site_url = row['사이트 주소']
                if site_url != '-':
                    # 여러 개의 URL이 있을 경우 첫 번째 것만 버튼으로, 나머지는 텍스트로
                    primary_url = site_url.split('\n')[0].strip()
                    st.link_button("🌐 공식 사이트 방문", primary_url)
                else:
                    st.write("사이트 정보 없음")

        if st.button(f"🚀 {target_company} 기술 기반 신제품 제안받기"):
            with st.spinner(f"AI가 {target_company}의 기술을 분석
