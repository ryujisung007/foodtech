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
            # 한글 인코딩 대응 (utf-8-sig 또는 cp949)
            df = pd.read_csv(file_path, encoding='utf-8-sig').fillna('-')
            return df
        except:
            return pd.read_csv(file_path, encoding='cp949').fillna('-')
    return pd.DataFrame()

def get_unique_categories(df, col, filters=None):
    """카테고리 유니크 값 추출"""
    tmp = df.copy()
    if filters:
        for c, v in filters.items():
            tmp = tmp[tmp[c] == v]
    return sorted(tmp[col].unique().tolist())

def get_filtered_results(df, mid, sub):
    """중분류 및 소분류 필터링 결과 반환"""
    return df[(df['중분류'] == mid) & (df['소분류'] == sub)]
