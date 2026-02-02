import streamlit as st

def render_sidebar(df, engine_data):
    """사이드바 필터 구성"""
    st.sidebar.header("🔍 검색 필터")
    
    # 데이터가 없을 경우 업로드 UI 제공
    if df.empty:
        st.sidebar.warning("⚠️ 파일을 찾을 수 없습니다.")
        uploaded_file = st.sidebar.file_uploader("foodtech_company.csv 업로드", type=['csv'])
        if uploaded_file is not None:
            import pandas as pd
            df_uploaded = pd.read_csv(uploaded_file)
            st.session_state['uploaded_df'] = df_uploaded
            st.rerun()
        return "선택하세요", "선택하세요"

    # 중분류 선택
    mid_categories = engine_data.get_unique_categories(df, '중분류')
    selected_mid = st.sidebar.selectbox("1. 중분류 선택", ["선택하세요"] + mid_categories)
    
    selected_sub = "선택하세요"
    if selected_mid != "선택하세요":
        # 소분류 선택 (중분류에 종속)
        sub_categories = engine_data.get_unique_categories(df, '소분류', {'중분류': selected_mid})
        selected_sub = st.sidebar.selectbox("2. 소분류 선택", ["선택하세요"] + sub_categories)
        
    return selected_mid, selected_sub

def render_results(filtered_df):
    """결과 테이블 렌더링"""
    if not filtered_df.empty:
        st.subheader(f"✅ 조회 결과 (총 {len(filtered_df)}개 기업)")
        
        # 표시할 컬럼 정의
        display_columns = ['기업이름', '기업정보', '대표기술', '대표제품', '사이트 주소']
        view_df = filtered_df[display_columns].reset_index(drop=True)

        # 데이터프레임 출력 - 괄호 및 설정값 오류 점검 완료
        st.dataframe(
            view_df,
            use_container_width=True,
            column_config={
                "기업이름": st.column_config.TextColumn("기업명", width="medium"),
                "기업정보": st.column_config.TextColumn("기업정보", width="large"),
                "대표기술": st.column_config.TextColumn("대표기술", width="medium"),
                "대표제품": st.column_config.TextColumn("대표제품", width="medium"),
                "사이트 주소": st.column_config.LinkColumn("사이트 주소", width="medium")
            },
            hide_index=True
        )
    else:
        st.info("해당 분류에 데이터가 존재하지 않습니다.")
