import streamlit as st
import engine_data
import ui_layout

st.set_page_config(page_title="푸드테크 AI 플랫폼", layout="wide")

def main():
    st.title("🚀 푸드테크 기업 정보 & AI R&D 플랫폼")
    
    df = engine_data.load_data()
    mid_cat, sub_cat = ui_layout.render_sidebar(df, engine_data)
    
    if not df.empty:
        if mid_cat != "선택하세요" and sub_cat != "선택하세요":
            filtered_df = engine_data.get_filtered_results(df, mid_cat, sub_cat)
            ui_layout.render_results(filtered_df, df) 
        else:
            st.info("왼쪽에서 분류를 선택하세요. 하단에서 챗봇 상담이 가능합니다.")
            ui_layout.render_chatbot(df)
    else:
        st.error("데이터가 로드되지 않았습니다.")

if __name__ == "__main__":
    main()
