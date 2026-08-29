import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("⚾ KBO 야구 공부 챗봇")
st.write(
    "KBO 리그의 야구 규칙과 다양한 야구 개념을 쉽게 설명해주는 챗봇입니다. "
    "야구를 처음 접하는 사람도 이해할 수 있도록 차근차근 설명해드립니다."
)

# Ask user for their OpenAI API key.
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("OpenAI API Key를 입력해주세요.", icon="🗝️")

else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing chat messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("야구 규칙이나 개념을 질문해보세요!"):

        # Store and display user message.
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                    당신은 KBO 야구 전문 지식과 야구 규칙을 쉽게 설명해주는
                    친절한 야구 선생님입니다.

                    사용자는 야구 초보자일 수 있으므로 어려운 야구 용어를
                    사용할 때는 반드시 쉽게 풀어서 설명해주세요.

                    특히 다음과 같은 주제에 대해 설명할 수 있습니다.

                    - 야구의 기본 규칙
                    - 스트라이크와 볼
                    - 아웃과 이닝
                    - 안타, 2루타, 3루타, 홈런
                    - 타율, 출루율, 장타율, OPS
                    - ERA, WHIP, 승리투수, 세이브
                    - 병살, 희생플라이, 희생번트
                    - 도루와 도루실패
                    - 포스 아웃과 태그 아웃
                    - 인필드 플라이
                    - 야수선택
                    - 지명타자
                    - 투수 교체 및 불펜
                    - KBO 리그의 경기 및 제도

                    설명할 때는 단순히 정의만 알려주지 말고,
                    가능하면 실제 야구 경기에서 어떤 상황에서 사용되는지
                    예시를 들어 설명해주세요.

                    사용자가 잘못 이해하고 있다면 부드럽게 바로잡아주세요.

                    KBO와 관련된 질문에서는 KBO 리그의 맥락을 우선적으로
                    고려해서 답변해주세요.

                    확실하지 않은 내용은 추측해서 답하지 말고,
                    모르는 부분은 모른다고 말해주세요.
                    """,
                },
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            ],
            stream=True,
        )

        # Stream response.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # Store assistant response.
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
