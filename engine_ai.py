import openai
import streamlit as st

def get_product_ideation(company_name, tech_info, product_info):
    """기존: 기업 기술 및 제품 기반 R&D 제안 (로직 유지)"""
    if "OPENAI_API_KEY" not in st.secrets:
        return "❌ 오류: Streamlit Secrets에 'OPENAI_API_KEY'가 설정되어 있지 않습니다."
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = f"당신은 식품기술사입니다... [기업명: {company_name}] [기술: {tech_info}] [소재: {product_info}] 분석 보고서를 작성하세요."
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "식품공학 전문가"}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI 생성 오류: {str(e)}"

def get_chatbot_response(messages, context_df=None):
    """신규: 기업 데이터를 참고하여 답변하는 챗봇 엔진"""
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        client = openai.OpenAI(api_key=api_key)
        
        # 기업 데이터를 텍스트 컨텍스트로 변환 (RAG 간이 구현)
        context_text = ""
        if context_df is not None and not context_df.empty:
            context_text = "참고할 기업 데이터:\n" + context_df[['기업이름', '중분류', '소분류', '대표기술', '대표제품']].to_string(index=False)

        system_message = {
            "role": "system", 
            "content": f"당신은 식품 R&D 어시스턴트입니다. 다음 데이터를 참고하여 사용자의 질문에 전문적으로 답변하세요. {context_text}"
        }
        
        # 시스템 메시지를 포함하여 전체 대화 전달
        chat_messages = [system_message] + messages
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_messages,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 챗봇 응답 오류: {str(e)}"
