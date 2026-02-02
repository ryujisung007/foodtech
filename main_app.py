import streamlit as st
import engine_data
import ui_layout

st.set_page_config(page_title="푸드테크 DB 조회", page_icon="🍲", layout="wide")

def main():
    st.title("🚀 푸드테크 기업 정보 통합 조회 시스템")
    
    df = engine_data.load_data()
    mid_cat, sub_cat = ui_layout.render_sidebar(df, engine_data)
    
    if not df.empty:
        if mid_cat != "선택하세요" and sub_cat != "선택하세요":
            filtered_df = engine_data.get_filtered_results(df, mid_cat, sub_cat)
            ui_layout.render_results(filtered_df)
        else:
            st.info("왼쪽 사이드바에서 카테고리를 선택해 주세요.")
    else:
        st.error("데이터가 로드되지 않았습니다. 사이드바를 통해 CSV 파일을 업로드해 주세요.")

if __name__ == "__main__":
    main()
