import google.generativeai as genai
import streamlit as st
import random

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_product_ideation(company, tech, product):
    """OpenAI/Gemini를 활용한 신제품 아이디어 생성 (빠른 응답 모델)"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            f"식품 R&D 전문가로서 '{company}'의 '{tech}' 기술과 '{product}' 제품을 분석해줘. "
            "이 소재를 활용한 혁신적인 신제품 아이디어 3가지와 사용 목적, 용도, 주의사항을 표 형태로 제안해줘."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI 분석 중 오류 발생: {e}"

def generate_nano_banana_images(tech, product, count=3):
    """나노 바나나(Imagen) 3개 생성 - 매번 다른 스타일 적용"""
    images = []
    styles = [
        "Professional food photography, cinematic lighting",
        "Modern minimal product packaging design, 3D render",
        "Artistic macro shot, studio lighting, high detail"
    ]
    try:
        model = genai.GenerativeModel('imagen-3.0-generate-001')
        for i in range(count):
            style = styles[i % len(styles)]
            prompt = f"{style} of food product concept using {tech} and {product}, 8k, unique_{random.randint(1,999)}"
            response = model.generate_content(prompt)
            if hasattr(response, 'images') and response.images:
                images.append(response.images[0])
    except:
        pass # 이미지 생성 실패 시 빈 리스트 반환
    return images
