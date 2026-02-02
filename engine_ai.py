import openai
import streamlit as st

def get_product_ideation(company_name, tech_info, product_info):
    if "OPENAI_API_KEY" not in st.secrets:
        return "❌ Secrets에 API 키가 없습니다."
    
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    prompt = f"기업 {company_name}의 기술({tech_info})과 소재({product_info})를 분석하여 아이스크림, 초콜릿, 코팅, 베이커리 분야 신제품을 제안하세요."
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "식품공학 전문가"}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 오류: {str(e)}"

def get_chatbot_response(messages, context_df):
    if "OPENAI_API_KEY" not in st.secrets:
        return "❌ API 키가 없습니다."
    
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    context = context_df[['기업이름', '중분류', '소분류', '대표기술', '대표제품']].to_string(index=False)
    
    system_msg = {"role": "system", "content": f"당신은 식품 R&D 전문가입니다. 아래 데이터를 숙지하고 답하세요.\n{context}"}
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[system_msg] + messages,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 챗봇 오류: {str(e)}"
