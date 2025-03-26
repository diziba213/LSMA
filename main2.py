import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# API 키 가져오기(getenv) api_key = os.getenv("OPENAI_API_KEY")

# API 키 가져오기 (st.secrets)
api_key = st.secrets["OPENAI_API_KEY"]

# OpenAI 클라이언트 생성
if api_key:
    client = OpenAI(api_key=api_key)
else:
    st.error("API key not found. Please set the OPENAI_API_KEY environment variable in your .env file.")

def fetch_combination_score(musician, company):
    prompt = f"Suggest a collaboration between the international musician '{musician}' and the South Korean entertainment company '{company}'. Provide a compatibility score between 0 and 1, and explain the reasoning."

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions="You are a helpful assistant.",
            input=prompt,
        )
        
        result = response.output_text.strip()
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

if st.button('Generate Suggestion'):
    result = fetch_combination_score(selected_musician, selected_company)
    st.write(result)
