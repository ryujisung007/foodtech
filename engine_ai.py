import openai
import streamlit as st

def get_product_ideation(company_name, tech_info, product_info):
    """기업의 대표기술 및 대표제품 소재를 활용한 4대 카테고리 아이디에이션"""
    
    if "OPENAI_API_KEY" not in st.secrets:
        return "❌ 오류: Streamlit Secrets에 'OPENAI_API_KEY'가 설정되어 있지 않습니다."

    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # [설계] 대표제품의 소재적 특성을 반영하도록 프롬프트 구성
        prompt = f"""
        당신은 20년 경력의 식품 R&D 전문가(식품기술사급)입니다. 
        다음 기업의 [대표기술]과 [대표제품]의 소재 특성을 분석하여 신제품 아이디어를 제안하세요.
        
        [기업명]: {company_name}
        [대표기술]: {tech_info}
        [대표제품(소재)]: {product_info}
        
        다음 4개 카테고리별로 제안하세요:
        1. 아이스크림 (Ice Cream): 소재의 유화/안정성 및 오버런(Overrun) 영향 분석을 포함한 제안
        2. 초콜릿 (Chocolate): 소재의 입자 크기 및 분산성, 풍미 결합 제안
        3. 초콜릿 코팅 (Confectionery Coating): 점도 제어 및 코팅력, 바삭함(Crispiness) 부여 제안
        4. 베이커리 (Bakery): 단백질 변성 및 전분 노화 억제 등 구조적 기여도 제안
        
        형식: 
        ### [카테고리명]
        - **제품명**: ...
        - **소재 적용 포인트**: {product_info}를 어떤 기능적 목적으로 사용했는지 설명
        - **R&D 인사이트**: 식품공학적 구현 핵심 (물성, 가공 조건 등)
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "식품공학 박사이자 소재 개발 전문가로서 실현 가능한 R&D 아이디어를 제안합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI 생성 중 오류 발생: {str(e)}"
