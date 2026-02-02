import streamlit as st
import engine_data
import ui_layout
import engine_ai

# 페이지 설정
st.set_page_config(
    page_title="푸드테크 기업 정보 시뮬레이터",
    page_icon="🍲",
    layout="wide"
)

def main():
    st.title("🚀 푸드테크 기업 정보 통합 조회 시스템")
    st.markdown("관심 있는 중분류와 소분류를 선택하여 관련 기업의 상세 기술 및 제품 정보를 확인하세요.")

    # 1. 데이터 로드
    df = engine_data.load_data()
    
    if not df.empty:
        # 2. 사이드바 UI 및 선택 값 취득
        mid_cat, sub_cat = ui_layout.render_sidebar(df, engine_data)
        
        # 3. 결과 표시 로직
        if mid_cat != "선택하세요" and sub_cat != "선택하세요":
            filtered_df = engine_data.get_filtered_results(df, mid_cat, sub_cat)
            ui_layout.render_results(filtered_df)
        else:
            st.warning("왼쪽 사이드바에서 카테고리를 모두 선택해 주세요.")

if __name__ == "__main__":
    main()
