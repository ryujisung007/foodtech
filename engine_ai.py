import openai
import streamlit as st

def get_product_ideation(company_name, tech_info, product_info):
    """기술(적용방안)과 소재(신소재 융합)를 구분하여 4대 제품군 아이디에이션 생성"""
    
    if "OPENAI_API_KEY" not in st.secrets:
        return "❌ 오류: Streamlit Secrets에 'OPENAI_API_KEY'가 설정되어 있지 않습니다."

    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # [R&D 전문 프롬프트 설계]
        prompt = f"""
        당신은 20년 경력의 식품 R&D 전문가(식품기술사)입니다. 
        [기업명: {company_name}]의 데이터를 바탕으로 다음 두 가지 관점에서 4대 카테고리(아이스크림, 초콜릿, 코팅, 베이커리)에 대한 전문 보고서를 작성하세요.

        1. [관점 A: 대표기술 활용] 보유기술({tech_info})을 활용한 구체적인 공정 및 제품 적용 방안
        2. [관점 B: 대표제품/소재 활용] 소재({product_info})를 접목한 신소재 적용 기술 및 구체적 제품 제안

        대상 카테고리:
        - 아이스크림, 초콜릿, 초콜릿 코팅, 베이커리

        응답 형식:
        ### 1. {company_name} 기술 및 소재 분석 요약
        - **기술 기반 적용 방안**: {tech_info}를 활용한 공정 최적화 및 적용 전략
        - **소재 기반 융합 전략**: {product_info}를 활용한 신소재화 및 제품화 전략

        ### 2. 카테고리별 R&D 제안
        #### [카테고리명]
        - **제품명**: ...
        - **[기술] 적용방안**: 이 기술을 공정에 어떻게 녹여낼 것인가?
        - **[소재] 신소재 적용 및 제안**: 이 소재를 활용한 새로운 가치 창출 제안
        - **R&D 포인트**: 식품공학적(물성, 안정성 등) 핵심 분석
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "식품공학 박사 수준의 R&D 인사이트를 제공합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI 생성 중 오류 발생: {str(e)}"
