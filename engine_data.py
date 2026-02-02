import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    if 'uploaded_df' in st.session_state:
        return st.session_state['uploaded_df']
    file_path = 'foodtech_company.csv'
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path, encoding='utf-8-sig').fillna('-')
        except:
            return pd.read_csv(file_path, encoding='cp949').fillna('-')
    return pd.DataFrame()

def get_unique_categories(df, col, filters=None):
    if df.empty: return []
    tmp = df.copy()
    if filters:
        for c, v in filters.items(): tmp = tmp[tmp[c] == v]
    return sorted(tmp[col].unique().tolist())

def get_filtered_results(df, mid, sub):
    return df[(df['중분류'] == mid) & (df['소분류'] == sub)]
