import openai
import streamlit as st

def get_product_ideation(company_name, tech_info):
    """기업 기술 기반 4대 카테고리 제품 아이디에이션 생성"""
    # 세션 스토어에서 API 키를 가져오거나 secrets에서 가져옵니다.
    # st.secrets["OPENAI_API_KEY"] 설정 권장
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    prompt = f"""
    당신은 20년 경력의 식품 R&D 전문가이자 마케팅 전략가입니다.
    다음 기업의 [대표기술]을 활용하여 4가지 카테고리에 맞는 혁신적인 신제품 아이디어를 제안하세요.
    
    [기업명]: {company_name}
    [대표기술]: {tech_info}
    
    다음 각 항목별로 제품명과 핵심 소구점(USP)을 한 줄로 요약하세요:
    1. 아이스크림: 
    2. 초콜렛: 
    3. 초콜렛코팅 (Confectionery coating): 
    4. 베이커리: 
    
    형식: 카테고리명: [제품명] - 내용
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # 반응 속도가 빠르고 효율적인 모델
            messages=[{"role": "system", "content": "식품 공학 박사 수준의 전문적인 제품 개발자 역량을 발휘하세요."},
                      {"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 생성 중 오류 발생: {str(e)}"
