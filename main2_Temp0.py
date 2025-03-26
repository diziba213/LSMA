import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# .env에서 환경변수 로드
load_dotenv()

# API 키 가져오기
api_key = st.secrets["general"]["OPENAI_API_KEY"]

# OpenAI 클라이언트 생성
if api_key:
    client = OpenAI(api_key=api_key)
else:
    st.error("API key not found.")

def fetch_combination_score(musician, company, temperature=0.0):
    prompt = (
        f"Suggest a collaboration between the international musician '{musician}' "
        f"and the South Korean entertainment company '{company}'. "
        "Provide a compatibility score between 0 and 1, "
        "and explain the reasoning within 500 characters."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=500  # 약 500자 내외의 분량
        )
        
        result = response.choices[0].message.content.strip()
        return result
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI 설정
st.title('🎵 Music Collaboration Suggestion App')
st.write('Explore potential collaborations between international musicians and Korean entertainment companies!')

musicians = [
    'Taylor Swift', 'BTS', 'Drake', 'Ed Sheeran', 'Billie Eilish', 
    'The Weeknd', 'Bad Bunny', 'Ariana Grande', 'Justin Bieber', 'Dua Lipa'
]

companies = [
    'HYBE', 'SM Entertainment', 'JYP Entertainment', 'YG Entertainment', 'CJ ENM'
]

selected_musician = st.selectbox('Select a Musician', musicians)
selected_company = st.selectbox('Select an Entertainment Company', companies)
temperature = st.slider('Temperature (Creativity Level)', min_value=0.0, max_value=1.5, value=0.0, step=0.1)

if st.button('Generate Suggestion'):
    result = fetch_combination_score(selected_musician, selected_company, temperature)
    st.write(result)
