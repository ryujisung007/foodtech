import pandas as pd
import streamlit as st
import os

def load_data():
    """DB 파일을 로드하고 컬럼명 및 데이터를 정제합니다."""
    file_name = 'foodtech_company.csv'
    if not os.path.exists(file_name):
        st.error(f"파일을 찾을 수 없습니다: {file_name}")
        return None
    try:
        # 한글 인코딩 및 컬럼명 공백 제거
        df = pd.read_csv(file_name, encoding='utf-8-sig')
        df.columns = [col.strip() for col in df.columns]
        # 데이터 내 줄바꿈 제거하여 프롬프트 가독성 향상
        df = df.replace(r'\n', ' ', regex=True)
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None
