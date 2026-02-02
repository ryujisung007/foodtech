import google.generativeai as genai
import streamlit as st
import random

# API 키 설정 (보안 강화)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets에 GEMINI_API_KEY가 없습니다.")

def get_product_ideation(company, tech, product):
    """제미나이를 이용해 신제품 R&D 아이디어 생성"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            f"식품 연구원 관점에서 {company}의 {tech} 기술과 {product} 제품을 분석해줘. "
            f"이 기술을 활용한 혁신적인 신제품 아이디어 3가지와 기대효과를 전문적으로 설명해줘."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"텍스트 생성 오류: {str(e)}"

def generate_nano_banana_images(tech, product, count=3):
    """나노 바나나(Imagen)를 호출하여 3개의 서로 다른 시안 생성"""
    image_list = []
    # 매번 다른 그림을 그리기 위한 스타일 셋
    styles = [
        "Professional food photography, top-down view",
        "Futuristic food packaging design, 3D render",
        "Close-up macro shot, artistic lighting"
    ]
    
    try:
        # 이미지 생성 전용 모델 설정
        model = genai.GenerativeModel('imagen-3.0-generate-001')
        
        for i in range(count):
            style_desc = styles[i % len(styles)]
            # 프롬프트에 랜덤 시드값을 포함하여 중복 생성 방지
            prompt = (
                f"{style_desc} of {product} concept using {tech}. "
                f"High resolution, 8k, commercial quality, "
                f"random_tag:{random.randint(1, 100000)}"
            )
            
            response = model.generate_content(prompt)
            
            # API 응답 객체에서 이미지 데이터 추출 (구조 확인 필수)
            if hasattr(response, 'images') and len(response.images) > 0:
                image_list.append(response.images[0])
                
    except Exception as e:
        st.error(f"이미지 생성 실패: {str(e)}")
        
    return image_list
