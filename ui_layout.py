import streamlit as st
import pandas as pd

def render_sidebar(df, engine_data):
    st.sidebar.header("🔍 검색 필터")
    
    # 데이터가 비어있을 경우 업로드 버튼 표시
    if df.empty:
        st.sidebar.warning("⚠️ CSV 파일을 찾을 수 없습니다.")
        uploaded_file = st.sidebar.file_uploader("foodtech_company.csv 파일을 선택하세요", type=['csv'])
        if uploaded_file is not None:
            df_uploaded = pd.read_csv(uploaded_file)
            st.session_state['uploaded_df'] = df_uploaded
            st.rerun()
        return "선택하세요", "선택하세요"

    # 중분류 선택
    mid_categories = engine_data.get_unique_categories(df, '중분류')
    selected_mid = st.sidebar.selectbox("1. 중분류 선택", ["선택하세요"] + mid_categories)
    
    selected_sub = "선택하세요"
    if selected_mid != "선택하세요":
        # 소분류 선택
        sub_categories = engine_data.get_unique_categories(df, '소분류', {'중분류': selected_mid})
        selected_sub = st.sidebar.selectbox("2. 소분류 선택", ["선택하세요"] + sub_categories)
        
    return selected_mid, selected_sub

def render_results(filtered_df):
    if not filtered_df.empty:
        st.subheader(f"✅ 검색 결과 (총 {len(filtered_df)}개 기업)")
        for idx, row in filtered_df.iterrows():
            with st.expander(f"🏢 {row['기업이름']}", expanded=True):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write(f"**🔹 기업정보:** {row['기업정보']}")
                    st.write(f"**🔹 대표기술:** {row['대표기술']}")
                with col2:
                    st.write(f"**🔹 대표제품:** {row['대표제품']}")
                    st.write(f"**🔗 사이트:** {row['사이트 주소']}")
    else:
        st.info("데이터를 선택하면 정보가 표시됩니다.")
