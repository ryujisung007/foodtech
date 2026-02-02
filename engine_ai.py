import google.generativeai as genai
import streamlit as st
import random

# API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_product_ideation(company, tech, product):
    """표준 모델 명칭을 사용하여 404 에러를 차단합니다."""
    # 모델명 리스트 (환경에 따라 작동하는 모델이 다를 수 있어 순차 시도)
    model_names = ['gemini-1.5-flash', 'gemini-pro']
    
    for m_name in model_names:
        try:
            model = genai.GenerativeModel(m_name)
            prompt = (
                f"당신은 식품 R&D 전략 전문가입니다. '{company}'의 '{tech}' 기술과 '{product}' 제품을 기반으로 "
                f"혁신적인 신제품 아이디어 3가지를 제안해 주세요. "
                f"반드시 [제품명, 사용목적, 용도, 용법, 사용주의사항]이 포함된 표 형식으로 작성해야 합니다."
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            continue # 실패 시 다음 모델로 시도
            
    return "⚠️ 현재 분석 엔진 서비스 점검 중입니다. 잠시 후 다시 시도해 주세요."

def generate_nano_banana_images(tech, product, count=3):
    """서로 다른 스타일의 시안 3개를 생성합니다."""
    image_list = []
    # 3가지 차별화된 컨셉 정의
    styles = [
        "Professional food photography, minimalist clean background, cinematic lighting",
        "Modern 3D product packaging design, laboratory aesthetic, 8k render",
        "Artistic macro photography showing food texture, vibrant colors, bokeh"
    ]
    
    try:
        # 이미지 생성 모델 설정 (가장 보편적인 모델명 사용)
        model = genai.GenerativeModel('imagen-3.0-generate-001')
        for i in range(count):
            style_desc = styles[i % len(styles)]
            prompt = (
                f"{style_desc} of a food product using {tech} and {product}. "
                f"High quality, photorealistic, variety_seed:{random.randint(1, 99999)}"
            )
            response = model.generate_content(prompt)
            if hasattr(response, 'images') and response.images:
                image_list.append(response.images[0])
    except Exception as e:
        # 에러 로그 출력 (개발 단계 확인용)
        print(f"이미지 생성 오류: {e}")
        
    return image_list
