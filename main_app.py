import streamlit as st
import engine_data
import ui_layout

def main():
    st.set_page_config(layout="wide", page_title="Food Tech R&D Simulator")
    st.title("🧪 식품 소재 및 제품 개발 시뮬레이터")

    # 데이터 로드
    df = engine_data.load_data()

    if df is not None:
        # 사이드바 필터링 (중분류, 소분류 기능 복구)
        st.sidebar.header("🔍 검색 필터")
        
        # 중분류 선택
        m_categories = ["전체"] + list(df['중분류'].unique())
        selected_m = st.sidebar.selectbox("중분류 선택", m_categories)
        
        filtered_df = df.copy()
        if selected_m != "전체":
            filtered_df = filtered_df[filtered_df['중분류'] == selected_m]
            
        # 소분류 선택
        s_categories = ["전체"] + list(filtered_df['소분류'].unique())
        selected_s = st.sidebar.selectbox("소분류 선택", s_categories)
        
        if selected_s != "전체":
            filtered_df = filtered_df[filtered_df['소분류'] == selected_s]
            
        # 기업이름 선택
        companies = ["전체"] + list(filtered_df['기업이름'].unique())
        selected_c = st.sidebar.selectbox("기업 선택", companies)
        
        if selected_c != "전체":
            filtered_df = filtered_df[filtered_df['기업이름'] == selected_c]

        # 결과 렌더링 호출 (TypeError 방지: 인자 1개 전달)
        ui_layout.render_results(filtered_df)

if __name__ == "__main__":
    main()
