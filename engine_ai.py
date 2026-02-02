import openai
import streamlit as st

def get_product_ideation(company_name, tech_info, product_info):
    """기업 기술 및 소재 기반 4대 카테고리 R&D 제안"""
    if "OPENAI_API_KEY" not in st.secrets:
        return "❌ 오류: Secrets에 'OPENAI_API_KEY'가 없습니다."
    
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    prompt = f"""
    당신은 식품기술사급 R&D 전문가입니다. 
    [기업명: {company_name}] 데이터를 분석하여 아이스크림, 초콜릿, 코팅, 베이커리 분야 신제품을 제안하세요.
    - [기술 활용]: {tech_info}를 활용한 공정 및 제품 적용 방안
    - [소재 활용]: {product_info}를 접목한 신소재 적용 기술 및 제품 제안
    전문적인 식품 공학 용어를 사용하여 보고서 형식으로 작성하세요.
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
    """기업 데이터를 참고하여 답변하는 R&D 챗봇 (오류 수정 완료)"""
    if "OPENAI_API_KEY" not in st.secrets:
        return "❌ 오류: API 키가 없습니다."
    
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # RAG: 데이터프레임을 텍스트 컨텍스트로 변환
    context = context_df[['기업이름', '중분류', '소분류', '대표기술', '대표제품']].to_string(index=False)
    system_msg = {
        "role": "system", 
        "content": f"당신은 식품 R&D 어시스턴트입니다. 아래의 푸드테크 기업 데이터를 숙지하고 사용자의 질문에 전문적으로 답변하세요. 데이터에 없는 내용은 일반적인 식품공학 지식에 기반하여 답하세요.\n\n[데이터]\n{context}"
    }
    
    try:
        # [수정 완료] 정식 OpenAI API 메소드 사용
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[system_msg] + messages,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 챗봇 오류: {str(e)}"
