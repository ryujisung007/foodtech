import streamlit as st
import engine_data
import ui_layout

# 페이지 설정
st.set_page_config(
    page_title="푸드테크 AI 플랫폼",
    page_icon="🍲",
    layout="wide"
)

def main():
    st.title("🚀 푸드테크 기업 정보 & AI R&D 플랫폼")
    
    # 1. 데이터 로드
    df = engine_data.load_data()
    
    # 2. 사이드바 렌더링 (중분류 -> 소분류 필터)
    mid_cat, sub_cat = ui_layout.render_sidebar(df, engine_data)
    
    # 3. 메인 결과 출력 및 챗봇 실행
    if not df.empty:
        if mid_cat != "선택하세요" and sub_cat != "선택하세요":
            filtered_df = engine_data.get_filtered_results(df, mid_cat, sub_cat)
            # 필터링된 데이터와 전체 데이터를 함께 전달
            ui_layout.render_results(filtered_df, df) 
        else:
            st.info("💡 왼쪽 사이드바에서 분류를 선택하세요. 하단 챗봇은 상시 이용 가능합니다.")
            ui_layout.render_chatbot(df)
    else:
        st.error("데이터 파일이 없습니다. CSV 파일을 업로드해 주세요.")

if __name__ == "__main__":
    main()
