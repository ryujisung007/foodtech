import pandas as pd
import streamlit as st

def load_data():
    """데이터 로드 및 텍스트 정제"""
    file_path = "foodtech_company.csv"
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        df.columns = [col.strip() for col in df.columns]
        # 데이터 내의 줄바꿈을 공백으로 치환하여 로직 오류 방지
        df = df.replace(r'\n', ' ', regex=True)
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return None
