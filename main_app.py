import streamlit as st
import pandas as pd
import engine_data
import ui_layout

def main():
    st.set_page_config(layout="wide", page_title="식품 R&D 시뮬레이터")
    
    st.title("🚀 식품 기술 및 제품 분석 대시보드")
    
    # 데이터 로드 (engine_data 모듈 사용)
    df = engine_data.load_data()
    
    if df is not None:
        # 사이드바에서 회사 선택
        selected_company = st.sidebar.selectbox("분석할 회사를 선택하세요", df['회사명'].unique())
        filtered_df = df[df['회사명'] == selected_company]
        
        # UI 레이아웃 호출
        ui_layout.render_results(filtered_df, df)

if __name__ == "__main__":
    main()
