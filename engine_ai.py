import google.generativeai as genai
import streamlit as st

def init_gemini():
    """Gemini API 설정 및 모델 초기화 (404 오류 해결 버전)"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # [수정 포인트] models/ 접두사를 제외하고 모델명만 입력해 보세요.
        # 만약 그래도 에러가 난다면 'gemini-1.5-flash-latest'로 시도할 수 있습니다.
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"Gemini 설정 실패: {e}")
        return None

def get_product_ideation(company_name, tech_info, product_info):
    """Gemini를 이용한 R&D 제안 (텍스트)"""
    model = init_gemini()
    if not model: return "API 연결 실패"

    prompt = f"""
    식품 R&D 전문가로서 [{company_name}]의 기술({tech_info})과 소재({product_info})를 분석하여 
    아이스크림, 초콜릿, 코팅, 베이커리 분야의 혁신 제품을 제안하세요.
    - 기술은 제품 적용방안 중심으로, 소재는 신소재 융합 기술 중심으로 설명하세요.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 에러 발생 시 상세 원인 파악을 위해 에러 문구 그대로 출력
        return f"💡 모델 호출 재시도 중 에러 발생: {str(e)}"
