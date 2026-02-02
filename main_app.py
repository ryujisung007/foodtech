import streamlit as st
import engine_data
import ui_layout

st.set_page_config(page_title="푸드테크 AI 시뮬레이터", page_icon="🍲", layout="wide")

# API 키 설정 (테스트용: 실제 환경에서는 .streamlit/secrets.toml 사용 권장)
if "OPENAI_API_KEY" not in st.secrets:
    st.sidebar.error("OpenAI API Key가 설정되지 않았습니다. Secrets에 등록해 주세요.")

def main():
    st.title("🚀 푸드테크 기업 정보 & AI 제품 아이디에이션")
    
    df = engine_data.load_data()
    mid_cat, sub_cat = ui_layout.render_sidebar(df, engine_data)
    
    if not df.empty:
        if mid_cat != "선택하세요" and sub_cat != "선택하세요":
            filtered_df = engine_data.get_filtered_results(df, mid_cat, sub_cat)
            ui_layout.render_results(filtered_df)
        else:
            st.info("왼쪽에서 분류를 선택하면 기업 목록과 AI 제안 기능이 활성화됩니다.")

if __name__ == "__main__":
    main()
