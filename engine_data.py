import pandas as pd
import streamlit as st

def load_data():
    """DB 파일을 로드하고 컬럼명 및 데이터를 정제합니다."""
    file_path = "foodtech_company.csv"
    try:
        # 한글 인코딩 및 데이터 정제
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        # 컬럼명 양끝 공백 제거
        df.columns = [col.strip() for col in df.columns]
        # 데이터 내의 불필요한 줄바꿈 제거
        df = df.replace(r'\n', ' ', regex=True)
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return None
