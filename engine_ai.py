import google.generativeai as genai
import streamlit as st

def init_gemini():
    """Gemini API 초기화 및 모델 연결 (404 오류 해결 버전)"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # v1beta 및 최신 버전 호환을 위한 모델 설정
        # 404 에러 발생 시 'gemini-1.5-flash' 혹은 'models/gemini-1.5-flash'로 교체 시도
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"Gemini API 설정 실패: {e}")
        return None

def get_product_ideation(company_name, tech_info, product_info):
    """Gemini 기반 4대 카테고리 R&D 제안"""
    model = init_gemini()
    if not model: return "API 연결을 확인해주세요."

    prompt = f"""
    당신은 식품공학 박사이자 식품기술사입니다.
    [{company_name}]의 기술({tech_info})과 소재({product_info})를 분석하여 
    아이스크림, 초콜릿, 초콜릿 코팅, 베이커리 4개 분야의 신제품을 제안하세요.
    - 기술은 적용방안 중심으로, 소재는 신소재 융합 기술 중심으로 설명하세요.
    - 전문적인 식품공학 용어(물성, 결정화, 기목적 등)를 사용하십시오.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"💡 모델 호출 오류: {str(e)}"

def get_chatbot_response(messages, context_df):
    """Gemini 기반 데이터 참조 챗봇"""
    model = init_gemini()
    if not model: return "챗봇 사용 불가"
    
    # RAG: 데이터프레임을 텍스트로 변환하여 컨텍스트 제공
    context = context_df[['기업이름', '중분류', '소분류', '대표기술', '대표제품']].to_string(index=False)
    system_instruction = f"당신은 식품 R&D 전문가입니다. 다음 데이터를 참고하여 답변하세요:\n{context}"
    
    try:
        full_prompt = f"{system_instruction}\n\n사용자 질문: {messages[-1]['content']}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"챗봇 오류: {e}"
