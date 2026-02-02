import google.generativeai as genai
import streamlit as st

def init_gemini():
    """가용한 최신 Gemini 모델을 자동으로 탐색하여 연결"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 가용 모델 리스트 필터링
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 우선순위: 1.5-flash -> 1.5-pro -> gemini-pro
        target_models = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        selected = next((m for m in target_models if m in available_models), 
                        available_models[0] if available_models else None)
        
        return genai.GenerativeModel(selected) if selected else None
    except Exception as e:
        st.error(f"Gemini 초기화 오류: {e}")
        return None

def get_product_ideation(company_name, tech_info, product_info):
    """식품공학 박사급 R&D 제안서 생성"""
    model = init_gemini()
    if not model: return "AI 모델을 불러올 수 없습니다."

    prompt = f"""
    당신은 식품공학 박사 및 식품기술사입니다.
    [{company_name}]의 기술({tech_info})과 소재({product_info})를 분석하여 
    아이스크림, 초콜릿, 초콜릿 코팅, 베이커리 4개 분야의 신제품을 제안하세요.
    - 특히 '식물성 계란(ALOK)'과 같은 메타텍스쳐 기술의 겔화(Gelation) 및 응고 특징을 기술하십시오.
    - 기술은 적용방안 중심으로, 소재는 신소재 융합 기술 중심으로 설명하세요.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"💡 호출 오류: {str(e)}"

def get_chatbot_response(messages, context_df):
    """RAG 기반 데이터 참조형 챗봇"""
    model = init_gemini()
    if not model or not messages: return "챗봇 응답 불가능"
    
    context = context_df[['기업이름', '중분류', '소분류', '대표기술', '대표제품']].to_string(index=False)
    system_instr = f"당신은 식품 R&D 전문가입니다. 다음 데이터를 참고하여 답변하세요:\n{context}"
    
    try:
        full_prompt = f"{system_instr}\n\n사용자 질문: {messages[-1]['content']}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"챗봇 오류: {str(e)}"
