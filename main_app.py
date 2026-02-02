import streamlit as st
import engine_data
import ui_layout

def main():
    st.set_page_config(layout="wide", page_title="Food Tech AI Simulator")
    st.title("🧪 식품 소재 및 제품 개발 시뮬레이터")

    df = engine_data.load_data()

    if df is not None:
        st.sidebar.header("🔍 검색 및 필터")
        
        # 필터링 체인
        m_list = ["전체"] + sorted(list(df['중분류'].unique()))
        selected_m = st.sidebar.selectbox("중분류", m_list)
        
        curr_df = df.copy()
        if selected_m != "전체":
            curr_df = curr_df[curr_df['중분류'] == selected_m]
            
        s_list = ["전체"] + sorted(list(curr_df['소분류'].unique()))
        selected_s = st.sidebar.selectbox("소분류", s_list)
        
        if selected_s != "전체":
            curr_df = curr_df[curr_df['소분류'] == selected_s]
            
        c_list = ["전체"] + sorted(list(curr_df['기업이름'].unique()))
        selected_c = st.sidebar.selectbox("기업 선택", c_list)
        
        if selected_c != "전체":
            curr_df = curr_df[curr_df['기업이름'] == selected_c]

        # UI 레이아웃 호출
        ui_layout.render_results(curr_df)

if __name__ == "__main__":
    main()
