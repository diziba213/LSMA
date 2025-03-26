import streamlit as st
import openai

# API 키 설정
openai.api_key = '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'

def fetch_combination_score(musician, company):
    prompt = f"Suggest a collaboration between the international musician '{musician}' and the South Korean entertainment company '{company}'. Provide a compatibility score between 0 and 1, and explain the reasoning."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # 또는 "gpt-4o-mini-2024-07-18"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        
        result = response.choices[0].message['content'].strip()
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