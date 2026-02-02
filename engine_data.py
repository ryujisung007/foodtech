import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    """데이터를 로드합니다. 파일 경로 문제 해결 로직 포함."""
    # 1. 세션에 업로드된 데이터가 우선
    if 'uploaded_df' in st.session_state:
        return st.session_state['uploaded_df']
        
    # 2. 로컬 파일 확인
    file_path = 'foodtech_company.csv'
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            df = df.fillna('-')
            return df
        except Exception as e:
            st.error(f"데이터 로드 오류: {e}")
            return pd.DataFrame()
    
    return pd.DataFrame()

def get_unique_categories(df, column_name, filter_dict=None):
    if df.empty: return []
    temp_df = df.copy()
    if filter_dict:
        for col, val in filter_dict.items():
            temp_df = temp_df[temp_df[col] == val]
    return sorted(temp_df[column_name].unique().tolist())

def get_filtered_results(df, mid_cat, sub_cat):
    if df.empty: return df
    return df[(df['중분류'] == mid_cat) & (df['소분류'] == sub_cat)]
