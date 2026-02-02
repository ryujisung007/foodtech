import streamlit as st
import engine_data
import ui_layout

def main():
    st.set_page_config(layout="wide", page_title="Food R&D Assistant")
    
    st.title("🧪 식품 소재 및 제품 개발 시뮬레이터")
    
    # 데이터 로드
    df = engine_data.load_data()
    
    if df is not None:
        # 사이드바에서 회사 선택
        company = st.sidebar.selectbox("대상 기업 선택", df['회사명'].unique())
        target_df = df[df['회사명'] == company]
        
        # 결과 출력 레이아웃 호출
        ui_layout.render_results(target_df, df)

if __name__ == "__main__":
    main()
