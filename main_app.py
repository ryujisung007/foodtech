import streamlit as st
import engine_data
import ui_layout

def main():
    st.set_page_config(layout="wide", page_title="Food Tech R&D")
    st.title("🚀 식품 R&D 제품 개발 시뮬레이터")

    df = engine_data.load_data()

    if df is not None:
        # KeyError 방지: '기업이름' 컬럼 존재 여부 확인
        if '기업이름' in df.columns:
            # 사이드바에서 기업 선택
            company_list = sorted(df['기업이름'].unique())
            selected = st.sidebar.selectbox("대상 기업 선택", company_list)
            
            target_df = df[df['기업이름'] == selected]
            ui_layout.render_results(target_df)
        else:
            st.error(f"컬럼명 오류. '기업이름' 컬럼이 필요합니다. 현재 컬럼: {list(df.columns)}")

if __name__ == "__main__":
    main()
