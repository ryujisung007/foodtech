import streamlit as st

def render_sidebar(df, engine_data):
    """사이드바에서 카테고리 선택 UI를 렌더링합니다."""
    st.sidebar.header("🔍 검색 필터")
    
    # 1. 중분류 선택
    mid_categories = engine_data.get_unique_categories(df, '중분류')
    selected_mid = st.sidebar.selectbox("1. 중분류 선택", ["선택하세요"] + mid_categories)
    
    selected_sub = "선택하세요"
    if selected_mid != "선택하세요":
        # 2. 소분류 선택 (중분류에 종속적)
        sub_categories = engine_data.get_unique_categories(df, '소분류', {'중분류': selected_mid})
        selected_sub = st.sidebar.selectbox("2. 소분류 선택", ["선택하세요"] + sub_categories)
        
    return selected_mid, selected_sub

def render_results(filtered_df):
    """필터링된 결과를 메인 화면에 표시합니다."""
    if not filtered_df.empty:
        st.subheader(f"✅ 검색 결과 (총 {len(filtered_df)}개 기업)")
        
        for idx, row in filtered_df.iterrows():
            with st.container():
                st.markdown(f"### 🏢 {row['기업이름']}")
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.write(f"**🔹 기업정보:** {row['기업정보']}")
                    st.write(f"**🔹 대표기술:** {row['대표기술']}")
                
                with col2:
                    st.write(f"**🔹 대표제품:** {row['대표제품']}")
                    st.write(f"**🔗 사이트 주소:** [{row['사이트 주소']}]({row['사이트 주소']})")
                
                st.divider()
    else:
        st.info("카테고리를 선택하면 기업 정보가 나타납니다.")
