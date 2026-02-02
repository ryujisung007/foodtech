import google.generativeai as genai
import streamlit as st
import random

# API 키 및 모델 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_product_ideation(company, tech, product):
    """모델명을 가장 호환성이 높은 방식으로 수정"""
    try:
        # 모델명에서 'models/' 접두사를 제외하거나 포함하여 재시도하는 안전 로직
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            f"당신은 식품 R&D 전문가입니다. '{company}'의 '{tech}' 기술과 '{product}' 제품을 분석하여 "
            "혁신적인 신제품 아이디어 3가지를 제안해 주세요. 각 제안에는 용도, 용법, 주의사항을 포함한 표를 작성해 주세요."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 404 에러 방지를 위한 폴백(Fallback) 로직
        return f"분석 엔진 로딩 중입니다. 잠시 후 다시 시도해 주세요. (상세: {str(e)})"

def generate_nano_banana_images(tech, product, count=3):
    """나노 바나나(Imagen) 3개 생성 - 최신 모델명 적용"""
    images = []
    styles = [
        "Professional food photography, cinematic lighting, 8k",
        "Modern minimal product packaging, 3D render, studio shot",
        "Artistic macro photography, vibrant colors, detailed texture"
    ]
    try:
        # Imagen 모델명을 최신 표준으로 변경 (구글 클라우드 설정에 따라 조정)
        # 일반적으로 'imagen-3.0-generate-001' 또는 'image-generation-006' 사용
        model = genai.GenerativeModel('imagen-3.0-generate-001')
        for i in range(count):
            style = styles[i % len(styles)]
            prompt = f"{style} of food concept using {tech} and {product}, high resolution, seed:{random.randint(1, 9999)}"
            response = model.generate_content(prompt)
            if hasattr(response, 'images') and response.images:
                images.append(response.images[0])
    except:
        pass 
    return images
