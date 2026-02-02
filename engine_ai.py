import google.generativeai as genai
import streamlit as st

def init_gemini():
    """Gemini API 초기화 및 모델 연결 (404 오류 방지 강화)"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # [해결책] 모델명을 'gemini-1.5-flash'로 단순화하여 호출합니다.
        # 만약 라이브러리 버전 문제로 404가 발생할 경우를 대비해 
        # 가장 호환성이 높은 모델명을 할당합니다.
        model_name = 'gemini-1.5-flash' 
        return genai.GenerativeModel(model_name)
    except Exception as e:
        st.error(f"Gemini API 설정 실패: {e}")
        return None

def get_product_ideation(company_name, tech_info, product_info):
    """Gemini 기반 4대 카테고리 R&D 제안 (텍스트 생성)"""
    model = init_gemini()
    if not model: return "API 설정 확인이 필요합니다."

    prompt = f"""
    당신은 식품공학 박사 및 식품기술사입니다.
    [{company_name}]의 기술({tech_info})과 소재({product_info})를 분석하여 
    아이스크림, 초콜릿, 초콜릿 코팅, 베이커리 4개 분야의 혁신 제품을 제안하세요.
    - 기술은 제품 적용방안 중심으로, 소재는 신소재 융합 기술 중심으로 설명하세요.
    - '식물성 계란(ALOK)' 등 메타텍스쳐 기술의 물성학적 특징을 강조하십시오.
    """
    try:
        # 모델 호출 시도
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 404 에러 발생 시 사용자에게 명확한 가이드 제공
        return f"💡 [연결 정보] 모델명을 'gemini-1.5-flash'로 확인해 주세요. (에러: {str(e)})"

def get_chatbot_response(messages, context_df):
    """Gemini 기반 데이터 참조 챗봇 (RAG)"""
    model = init_gemini()
    if not model: return "챗봇 초기화 실패"
    
    # 데이터 컨텍스트 구성
    context = context_df[['기업이름', '중분류', '소분류', '대표기술', '대표제품']].to_string(index=False)
    system_instruction = f"당신은 식품 R&D 전문가입니다. 다음 데이터를 참고하여 답변하세요:\n{context}"
    
    try:
        # 사용자 질문에 컨텍스트 결합
        full_prompt = f"{system_instruction}\n\n사용자 질문: {messages[-1]['content']}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"챗봇 응답 중 오류 발생: {str(e)}"
