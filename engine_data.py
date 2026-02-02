import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """CSV 데이터를 로드합니다."""
    try:
        df = pd.read_csv('foodtech_company.csv')
        # 데이터 클렌징: 개행문자 처리 등
        df = df.fillna('-')
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

def get_unique_categories(df, column_name, filter_dict=None):
    """특정 컬럼의 유니크한 값들을 반환합니다 (필터링 조건 포함 가능)."""
    temp_df = df.copy()
    if filter_dict:
        for col, val in filter_dict.items():
            temp_df = temp_df[temp_df[col] == val]
    return sorted(temp_df[column_name].unique().tolist())

def get_filtered_results(df, mid_cat, sub_cat):
    """중분류와 소분류로 필터링된 기업 데이터를 반환합니다."""
    return df[(df['중분류'] == mid_cat) & (df['소분류'] == sub_cat)]
