import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    """CSV 데이터를 로드하고 전처리를 수행합니다."""
    if 'uploaded_df' in st.session_state:
        return st.session_state['uploaded_df']
    
    file_path = 'foodtech_company.csv'
    if os.path.exists(file_path):
        try:
            # utf-8-sig로 인코딩 오류 방지
            df = pd.read_csv(file_path, encoding='utf-8-sig').fillna('-')
            return df
        except:
            # 실패 시 cp949 재시도
            return pd.read_csv(file_path, encoding='cp949').fillna('-')
    return pd.DataFrame()

def get_unique_categories(df, col, filters=None):
    """카테고리 목록 추출"""
    tmp = df.copy()
    if filters:
        for c, v in filters.items():
            tmp = tmp[tmp[c] == v]
    return sorted(tmp[col].unique().tolist())

def get_filtered_results(df, mid, sub):
    """중분류 및 소분류 필터링"""
    return df[(df['중분류'] == mid) & (df['소분류'] == sub)]
