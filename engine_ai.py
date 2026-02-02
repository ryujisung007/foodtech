import openai
import streamlit as st

def get_product_ideation(company_name, tech_info):
    """기업 기술 기반 4대 카테고리 제품 아이디에이션 생성"""
    
    # [설계] 별도 입력창 없이 st.secrets 내부의 OPENAI_API_KEY 참조
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        client = openai.OpenAI(api_key=api_key)
    except KeyError:
        return "❌ 오류: Streamlit Secrets에 'OPENAI_API_KEY'가 설정되어 있지 않습니다."

    prompt = f"""
    당신은 20년 경력의 식품 R&D 전문가(식품기술사급)입니다. 
    다음 기업의 핵심 기술을 분석하여 4가지 카테고리에 적용 가능한 혁신적인 제품 아이디어를 제안하세요.
    
    [기업명]: {company_name}
    [보유기술]: {tech_info}
    
    다음 각 항목별로 '제품명', '기술적 개발 컨셉', 'R&D 핵심 포인트'를 포함하여 전문적으로 제안하세요:
    1. 아이스크림 (Ice Cream)
    2. 초콜릿 (Chocolate)
    3. 초콜릿 코팅 (Confectionery Coating)
    4. 베이커리 (Bakery)
    
    응답 형식: 
    ### [카테고리명]
    - **제품명**: 000
    - **개발 컨셉**: 기술 응용 방식 설명
    - **R&D 포인트**: 식품 공학적 관점의 구현 핵심 (예: 물성 제어, 유화 안정성, 기목적 등)
    """
    
    try:
        # 반응 속도가 빠르고 효율적인 gpt-4o-mini 모델 사용
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
