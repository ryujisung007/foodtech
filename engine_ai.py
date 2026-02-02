import google.generativeai as genai
import streamlit as st

def init_gemini():
    """Gemini API 초기화"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Gemini API 키를 확인하세요: {e}")
        return None

def get_product_ideation(company_name, tech_info, product_info):
    """Gemini 기반 R&D 아이디에이션"""
    model = init_gemini()
    if not model: return "API 설정 오류"

    prompt = f"""
    당신은 식품공학 박사 및 식품기술사입니다.
    [{company_name}]의 기술({tech_info})과 소재({product_info})를 분석하여
    아이스크림, 초콜릿, 초콜릿 코팅, 베이커리 4개 분야의 혁신 제품을 제안하세요.
    - 기술은 적용방안 중심으로, 소재는 신소재 융합 기술 중심으로 설명하세요.
    - 전문적인 식품공학 용어를 사용하십시오.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"생성 오류: {e}"

def get_chatbot_response(messages, context_df):
    """Gemini 기반 R&D 챗봇"""
    model = init_gemini()
    context = context_df[['기업이름', '중분류', '소분류', '대표기술', '대표제품']].to_string(index=False)
    system_instruction = f"당신은 식품 R&D 어시스턴트입니다. 다음 데이터를 숙지하고 답하세요: \n{context}"
    
    try:
        # 메시지 포맷 변환 및 전송
        chat = model.start_chat(history=[])
        response = chat.send_message(f"{system_instruction}\n\n사용자 질문: {messages[-1]['content']}")
        return response.text
    except Exception as e:
        return f"챗봇 오류: {e}"
