import openai
import streamlit as st

def get_product_ideation(company_name, tech_info, product_info):
    """기업 기술 및 소재 기반 4대 카테고리 R&D 제안"""
    if "OPENAI_API_KEY" not in st.secrets:
        return "❌ 오류: Secrets에 'OPENAI_API_KEY'가 없습니다."
    
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    prompt = f"""
    당신은 식품기술사급 R&D 전문가입니다. 
    [기업명: {company_name}]의 기술({tech_info})과 소재({product_info})를 분석하여 
    아이스크림, 초콜릿, 코팅, 베이커리 분야의 혁신 제품을 제안하세요.
    기술은 적용방안 중심으로, 소재는 신소재 융합 기술 중심으로 서술하십시오.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "식품공학 박사급 인사이트 제공"}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI 생성 오류: {str(e)}"

def get_chatbot_response(messages, context_df):
    """기업 데이터를 참고하여 답변하는 R&D 챗봇"""
    if "OPENAI_API_KEY" not in st.secrets:
        return "❌ 오류: API 키가 없습니다."
    
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    context = context_df[['기업이름', '중분류', '소분류', '대표기술', '대표제품']].to_string(index=False)
    
    system_msg = {"role": "system", "content": f"당신은 식품 R&D 어시스턴트입니다. 다음 데이터를 참고하여 답변하세요:\n{context}"}
    try:
        response = client.chat.this_is_a_placeholder_for_chat_completions_create( # 명칭 확인용
            model="gpt-4o-mini",
            messages=[system_msg] + messages,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 챗봇 오류: {str(e)}"
