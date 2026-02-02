import google.generativeai as genai
import streamlit as st

def init_gemini():
    """Gemini API 설정 및 모델 초기화 (404 오류 해결 버전)"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 모델 경로를 명확히 지정 (v1beta 환경 대응)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"Gemini 설정 오류: {e}")
        return None

def get_product_ideation(company_name, tech_info, product_info):
    """Gemini 기반 R&D 아이디에이션 텍스트 생성"""
    model = init_gemini()
    if not model: return "API 초기화 실패"

    prompt = f"""
    당신은 식품공학 박사이자 식품기술사입니다.
    기업 [{company_name}]의 기술({tech_info})과 소재({product_info})를 분석하여 
    아이스크림, 초콜릿, 초콜릿 코팅, 베이커리 4개 분야의 혁신 제품을 제안하세요.
    - 기술은 제품 적용방안 중심으로, 소재는 신소재 융합 기술 중심으로 설명하세요.
    - 전문적인 식품공학 용어를 사용하여 상세히 서술하십시오.
    """
    try:
        # generate_content 호출 (404 발생 시 모델 식별자 재확인 필요)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"텍스트 생성 중 오류 발생: {e}"

def get_chatbot_response(messages, context_df):
    """Gemini 기반 R&D 챗봇 응답 생성"""
    model = init_gemini()
    if not model: return "챗봇 초기화 실패"
    
    context = context_df[['기업이름', '중분류', '소분류', '대표기술', '대표제품']].to_string(index=False)
    system_instruction = f"당신은 식품 R&D 전문가입니다. 다음 데이터를 참고하여 답변하세요:\n{context}"
    
    try:
        # 최신 메시지 기반 응답 생성
        full_prompt = f"{system_instruction}\n\n사용자 질문: {messages[-1]['content']}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"챗봇 응답 중 오류 발생: {e}"
