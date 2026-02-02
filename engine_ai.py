import openai
import streamlit as st

def get_product_ideation(company_name, tech_info):
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        client = openai.OpenAI(api_key=api_key)
    except KeyError:
        return "❌ 오류: Streamlit Secrets에 'OPENAI_API_KEY'가 설정되어 있지 않습니다."

    prompt = f"""
    당신은 20년 경력의 식품 R&D 전문가입니다. 
    다음 기업의 핵심 기술을 분석하여 아이스크림, 초콜릿, 초콜릿 코팅, 베이커리에 적용 가능한 혁신적인 제품 아이디어를 제안하세요.
    
    [기업명]: {company_name}
    [보유기술]: {tech_info}
    
    형식:
    ### [카테고리명]
    - **제품명**: 000
    - **개발 컨셉**: 기술 응용 방식
    - **R&D 포인트**: 식품 공학적 구현 핵심
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "식품공학 전문가로서 실현 가능한 R&D 아이디어를 제안합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI 생성 중 오류 발생: {str(e)}"
