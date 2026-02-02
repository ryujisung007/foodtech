import google.generativeai as genai
import streamlit as st
import random

# API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_product_ideation(company, tech, product):
    """제미나이를 이용한 전문 R&D 아이디어 생성 (빠른 응답 모델 사용)"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            f"식품공학 전문가로서 {company}의 {tech} 기술과 {product}을 분석하여 "
            "혁신적인 신제품 아이디어 3가지와 타당성을 제안해줘."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"분석 오류: {e}"

def generate_nano_banana_images(tech, product, count=3):
    """나노 바나나(Imagen)를 통해 3개의 서로 다른 시안 생성"""
    image_list = []
    # 중복 생성을 방지하기 위한 다양한 스타일 프롬프트
    styles = [
        "Professional food photography, cinematic lighting, 8k",
        "Minimalist product design, studio background, high detail",
        "Creative conceptual art, vibrant colors, photorealistic"
    ]
    
    try:
        model = genai.GenerativeModel('imagen-3.0-generate-001')
        for i in range(count):
            style_desc = styles[i % len(styles)]
            prompt = (
                f"{style_desc} of {product} using {tech} technology. "
                f"variation_id: {random.randint(1, 100000)}"
            )
            response = model.generate_content(prompt)
            if hasattr(response, 'images') and response.images:
                image_list.append(response.images[0])
    except Exception as e:
        print(f"이미지 생성 실패: {e}")
    return image_list
