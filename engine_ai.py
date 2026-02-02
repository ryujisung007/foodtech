import google.generativeai as genai
import streamlit as st
import random

# API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_product_ideation(company, tech, product):
    """표준 모델명을 사용하여 404 에러를 방지하고 아이디어를 생성합니다."""
    try:
        # 모델명을 단순화하여 호환성 확보
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            f"당신은 식품 R&D 전략 전문가입니다. '{company}'의 '{tech}' 기술과 '{product}' 제품을 기반으로 "
            f"혁신적인 신제품 아이디어 3가지를 제안해 주세요. "
            f"반드시 [제품명, 사용목적, 용도, 용법, 사용주의사항]이 포함된 표 형식으로 작성해야 합니다."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ 분석 엔진 연결 중: {str(e)}"

def generate_nano_banana_images(tech, product, count=3):
    """각기 다른 스타일의 이미지 3개를 생성합니다."""
    image_list = []
    # 3가지 차별화된 스타일 정의
    styles = [
        "Professional studio food photography, clean minimalist background, 8k",
        "Futuristic 3D digital render of food packaging, cinematic lighting",
        "Close-up macro shot of ingredients, vibrant colors, artistic bokeh"
    ]
    try:
        # 나노 바나나(Imagen) 모델 설정
        model = genai.GenerativeModel('imagen-3.0-generate-001')
        for i in range(count):
            style_desc = styles[i % len(styles)]
            prompt = (
                f"{style_desc} showing a new food concept using {tech} and {product}. "
                f"High quality, realistic, variety_seed:{random.randint(1, 99999)}"
            )
            response = model.generate_content(prompt)
            if hasattr(response, 'images') and response.images:
                image_list.append(response.images[0])
    except:
        pass 
    return image_list
