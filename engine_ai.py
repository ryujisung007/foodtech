import openai
import streamlit as st

def get_product_ideation(company_name, tech_info, product_info):
    """기업 기술 및 제품 기반 4대 카테고리 R&D 제안"""
    
    # Secrets 키 존재 여부 확인
    if "OPENAI_API_KEY" not in st.secrets:
        return "❌ 오류: Streamlit Secrets에 'OPENAI_API_KEY'가 설정되어 있지 않습니다."

    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        prompt = f"""
        당신은 20년 경력의 식품 R&D 전문가(식품기술사)입니다. 
        [기업명: {company_name}]의 데이터를 바탕으로 전문 보고서를 작성하세요.

        1. [기술 적용]: 보유기술({tech_info})을 활용한 공정 및 제품 적용 방안
        2. [소재 적용]: 소재({product_info})를 접목한 신소재 적용 기술 및 제품 제안

        대상 카테고리: 아이스크림, 초콜릿, 초콜릿 코팅, 베이커리

        응답 형식:
        ### 1. 기술 및 소재 분석 요약
        - **기술 기반 적용 방안**: 구체적 전략
        - **소재 기반 융합 전략**: 구체적 전략

        ### 2. 카테고리별 R&D 제안
        각 카테고리별 제품명, 기술 적용방안, 소재 적용기술 및 제안을 포함하세요.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "식품공학 박사 수준의 인사이트를 제공하는 R&D 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI 생성 중 오류 발생: {str(e)}"
