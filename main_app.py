import streamlit as st
import engine_data
import ui_layout

# 페이지 설정
st.set_page_config(
    page_title="푸드테크 기업 정보 시뮬레이터",
    page_icon="🍲",
    layout="wide" # 테이블을 넓게 보기 위해 와이드 모드 유지
)

def main():
    st.title("🚀 푸드테크 기업 정보 통합 조회 시스템")
    st.markdown("관심 있는 중분류와 소분류를 선택하여 기업 데이터를 테이블 형태로 확인하세요.")

    # 1. 데이터 로드
    df = engine_data.load_data()
    
    # 2. 사이드바 UI 및 선택 값 취득
    mid_cat, sub_cat = ui_layout.render_sidebar(df, engine_data)
    
    # 3. 결과 표시 로직
    if not df.empty:
        if mid_cat != "선택하세요" and sub_cat != "선택하세요":
            filtered_df = engine_data.get_filtered_results(df, mid_cat, sub_cat)
            ui_layout.render_results(filtered_df) # 수정된 테이블 렌더링 함수 호출
        else:
            st.info("💡 왼쪽 사이드바에서 **중분류**와 **소분류**를 선택해 주세요.")
    else:
        st.error("데이터 파일(foodtech_company.csv)이 없습니다. 사이드바에서 파일을 업로드해 주세요.")

if __name__ == "__main__":
    main()
