import google.generativeai as genai
import streamlit as st
import random

# API 키 설정 (Streamlit Secrets 활용)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_product_ideation(company, tech, product):
    """제미나이를 이용해 제품 및 기술 제안 텍스트 생성"""
    model = genai.GenerativeModel('gemini-1.5-flash') # 속도와 효율 중심
    prompt = f"{company}의 {tech} 기술과 {product} 제품을 분석하여, 이를 활용한 식품 R&D 신제품 아이디어와 기술 적용 방안을 설명해줘."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"텍스트 생성 중 오류 발생: {e}"

def generate_nano_banana_images(tech, product, count=3):
    """나노 바나나(Imagen)를 사용하여 3개의 서로 다른 추천 이미지를 생성"""
    # Imagen 모델 설정 (모델명은 실제 사용 가능한 최신 버전 기준)
    # 실제 Imagen API 호출 구조는 라이브러리 버전에 따라 다를 수 있으므로 표준 구조로 작성함
    images = []
    
    # 이미지별 다양성을 위한 스타일 셋
    styles = ["Hyper-realistic photography", "Futuristic 3D render", "Minimalist professional studio shot"]
    
    for i in range(count):
        style = styles[i % len(styles)]
        # 동일한 그림을 방지하기 위해 스타일과 랜덤 요소를 섞은 상세 프롬프트 생성
        prompt = (
            f"{style} of a new food product concept using {tech} and {product}. "
            f"High resolution, 8k, professional food styling, creative lighting, "
            f"variation_{random.randint(1, 1000)}"
        )
        
        try:
            # 나노 바나나(Imagen) 호출 로직
            model = genai.GenerativeModel('imagen-3.0-generate-001') 
            response = model.generate_content(prompt)
            # 성공 시 이미지 리
