import google.generativeai as genai
import streamlit as st

def init_gemini():
    """Gemini API 설정 및 모델 초기화"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # 텍스트 모델
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"Gemini 설정 오류: {e}")
        return None

def get_product_ideation(company_name, tech_info, product_info):
    """Gemini를 이용한 4대 카테고리 R&D 제안 (텍스트)"""
    model = init_gemini()
    if not model: return "API 연결 실패"

    prompt = f"""
    식품 R&D 전문가로서 [{company_name}]의 기술({tech_info})과 소재({product_info})를 분석하여 
    아이스크림, 초콜릿, 코팅, 베이커리 신제품을 제안하세요. 
    각 카테고리별로 '제품명', '기술적 구현방안', '소재 융합 포인트'를 상세히 설명하세요.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"제안 생성 중 오류: {e}"

def generate_concept_image(prompt_text):
    """나노 바나나(Imagen) 모델을 통한 식품 컨셉 이미지 생성"""
    # 주의: 현재 Gemini API를 통한 이미지 생성은 Imagen 모델 접근 권한이 필요합니다.
    # 아래는 표준적인 Image Generation 호출 구조의 예시입니다.
    try:
        # 이미지 생성을 위한 프롬프트 정제
        image_prompt = f"Professional food photography of {prompt_text}, high resolution, studio lighting, 4k"
        
        # 실제 환경에서는 Imagen API 또는 모델명을 설정해야 합니다.
        # 여기서는 Gemini가 생성한 텍스트를 기반으로 이미지를 생성하는 프로세스를 정의합니다.
        # (구글 클라우드 AI 플랫폼 연동 시나리오 기반)
        model = genai.GenerativeModel('imagen-3') # 최신 이미지 모델 가정
        result = model.generate_content(image_prompt)
        
        # 생성된 이미지 바이트 또는 URL 반환
        return result.images[0] # 첫 번째 이미지 객체
    except:
        # 이미지 생성 API 접근 불가 시 샘플 이미지 또는 에러 처리
        return None
