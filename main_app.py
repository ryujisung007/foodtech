import streamlit as st
import engine_data
import ui_layout

# 페이지 설정
st.set_page_config(
    page_title="푸드테크 AI 제품 시뮬레이터",
    page_icon="🍲",
    layout="wide"
)

def main():
    st.title("🚀 푸드테크 기업 정보 & AI 제품 아이디에이션")
    st.markdown("식품공학 전문가를 위한 기술 및 소재 기반 신제품 창작 플랫폼입니다.")

    # 1. 데이터 로드
    df = engine_data.load_data()
    
    # 2. 사이드바 렌더링 (분류 선택)
    mid_cat, sub_cat = ui_layout.render_sidebar(df, engine_data)
    
    # 3. 메인 결과 출력
    if not df.empty:
        if mid_cat != "선택하세요" and sub_cat != "선택하세요":
            filtered_df = engine_data.get_filtered_results(df, mid_cat, sub_cat)
            ui_layout.render_results(filtered_df)
        else:
            st.info("💡 왼쪽 사이드바에서 중분류와 소분류를 선택하여 조회를 시작하세요.")
    else:
        st.error("데이터가 없습니다. CSV 파일을 업로드해 주세요.")

if __name__ == "__main__":
    main()
