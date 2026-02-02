import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    """데이터 로드 및 세션 관리"""
    if 'uploaded_df' in st.session_state:
        return st.session_state['uploaded_df']
        
    file_path = 'foodtech_company.csv'
    if os.path.exists(file_path):
        try:
            # 인코딩 문제 방지를 위해 utf-8-sig 또는 cp949 고려 가능
            df = pd.read_csv(file_path)
            df = df.fillna('-')
            return df
        except Exception as e:
            st.error(f"데이터 파일 읽기 실패: {e}")
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
