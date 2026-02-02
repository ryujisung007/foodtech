import google.generativeai as genai
import streamlit as st

def init_gemini():
    """사용 가능한 최신 Gemini 모델을 자동으로 찾아 연결 (404 에러 해결)"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 1. 현재 API 키로 접근 가능한 모델 리스트 조회
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 2. 우선순위별 자동 매칭
        target_priorities = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        
        selected_model = None
        for target in target_priorities:
            if target in available_models:
                selected_model = target
                break
        
        # 3. 매칭 실패 시 가용 모델 중 첫 번째 선택
        if not selected_model and available_models:
            selected_model = available_models[0]
            
        return genai.GenerativeModel(selected_model) if selected_model else None
            
    except Exception as e:
        st.error(f"Gemini API 설정 실패: {e}")
        return None

def get_product_ideation(company_name, tech_info, product_info):
    """Gemini 기반 R&D 제안 생성"""
    model = init_gemini()
    if not model: return "모델 연결에 실패했습니다."

    prompt = f"""
    당신은 식품공학 박사 및 식품기술사입니다.
    [{company_name}]의 기술({tech_info})과 소재({product_info})를 분석하여 
    아이스크림, 초콜릿, 초콜릿 코팅, 베이커리 4개 분야의 혁신 제품을 제안하세요.
    - 특히 '메타텍스쳐(ALOK 등)' 기술의 물성학적 특징(응고, 유화, 겔화)을 강조하십시오.
    - 기술은 제품 적용방안 중심으로, 소재는 신소재 융합 기술 중심으로 설명하세요.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"💡 호출 오류: {str(e)}"

def get_chatbot_response(messages, context_df):
    """데이터 참조형 R&D 챗봇 (RAG)"""
    model = init_gemini()
    if not model: return "챗봇 초기화 실패"
    
    context = context_df[['기업이름', '중분류', '소
