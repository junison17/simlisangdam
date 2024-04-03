import streamlit as st
from openai import OpenAI

# Streamlit 애플리케이션 제목 설정
st.title("심리치유봇")

# OpenAI API 키 입력받기
api_key = st.text_input("OpenAI API 키를 입력하세요.", type="password")

# 대화 내용을 저장할 리스트 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {
            "role": "system",
            "content": " You are a chatbot that speaks Korean very fluently and writes Korean very well. You are a psychotherapist, listening to the user's worries and trying to solve their problems and heal their broken hearts.You are good at writing words that move the user, like a world-famous quoter. You have the wisdom of the Talmud, the eloquence of Helen Keller, and the words of famous quoters like Goethe, Mother Teresa, Tolstoy, Albert Einstein, Schopenhauer, Nietzsche, Socrates, Gandhi, Mencius, Nancy Sullivan, and Sophocles. Use natural colloquialisms, and use quotes from famous people occasionally, not a lot."
        }
    ]

# 대화 내용 출력
for message in st.session_state['messages'][1:]:
    if message['role'] == 'user':
        st.write(f"휴먼: {message['content']}")
    else:
        st.write(f"AI: {message['content']}")

def generate_response():
    if st.session_state.user_input:
        # OpenAI API 클라이언트 생성
        client = OpenAI(api_key=api_key)

        # 사용자 메시지 추가
        st.session_state['messages'].append({"role": "user", "content": st.session_state.user_input.strip()})

        # 챗봇 응답 생성
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=st.session_state['messages'],
            temperature=0.7,
            max_tokens=2500,
            top_p=1
        )

        # 응답 데이터 확인
        if response and response.choices and response.choices[0].message:
            # 챗봇 응답 추가
            st.session_state['messages'].append({"role": "assistant", "content": response.choices[0].message.content})
        else:
            st.session_state['messages'].append({"role": "assistant", "content": "챗봇 응답을 생성하는 데 실패했습니다."})

        # 사용자 입력 필드 초기화
        st.session_state.user_input = ""

# 사용자 입력을 받는 텍스트 입력 필드
user_input = st.text_input("글을 입력하세요:", key="user_input", on_change=generate_response)