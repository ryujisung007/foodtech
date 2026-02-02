import streamlit as st
import engine_data
import ui_layout

def main():
    st.set_page_config(layout="wide", page_title="Food Tech AI Simulator")
    st.title("🧪 식품 소재 및 제품 개발 시뮬레이터")

    df = engine_data.load_data()

    if df is not None:
        # 사이드바 필터링 로직
        st.sidebar.header("🔍 검색 필터")
        
        # 중분류 필터
        m_list = ["전체"] + sorted(list(df['중분류'].unique()))
        selected_m = st.sidebar.selectbox("중분류", m_list)
        
        tmp_df = df.copy()
        if selected_m != "전체":
            tmp_df = tmp_df[tmp_df['중분류'] == selected_m]
            
        # 소분류 필터
        s_list = ["전체"] + sorted(list(tmp_df['소분류'].unique()))
        selected_s = st.sidebar.selectbox("소분류", s_list)
        
        if selected_s != "전체":
            tmp_df = tmp_df[tmp_df['소분류'] == selected_s]
            
        # 기업 선택
        c_list = ["전체"] + sorted(list(tmp_df['기업이름'].unique()))
        selected_c = st.sidebar.selectbox("기업 선택", c_list)
        
        if selected_c != "전체":
            tmp_df = tmp_df[tmp_df['기업이름'] == selected_c]

        # UI 레이아웃 호출
        ui_layout.render_results(tmp_df)

if __name__ == "__main__":
    main()
