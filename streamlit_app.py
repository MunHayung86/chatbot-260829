```python
import streamlit as st
from openai import OpenAI


# ============================================================
# 페이지 설정
# ============================================================

st.set_page_config(
    page_title="KBO Baseball",
    page_icon="⚾",
    layout="centered",
)


# ============================================================
# CSS - 화면 디자인
# ============================================================

st.markdown(
    """
    <style>

    /* 전체 배경 */
    .stApp {
        background-color: #F7F8FA;
    }

    /* 기본 여백 */
    .block-container {
        max-width: 900px;
        padding-top: 3rem;
        padding-bottom: 5rem;
    }

    /* 제목 */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.3rem;
    }

    /* 부제목 */
    .sub-title {
        font-size: 17px;
        color: #6B7280;
        margin-bottom: 2rem;
    }

    /* 카테고리 카드 */
    .category-card {
        background-color: white;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 12px;
        min-height: 120px;
    }

    .category-title {
        font-size: 18px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 5px;
    }

    .category-description {
        font-size: 14px;
        color: #6B7280;
        line-height: 1.5;
    }

    /* 질문 안내 */
    .question-guide {
        background-color: white;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        padding: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* 버튼 */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        background-color: white;
        padding: 0.6rem 1rem;
        text-align: left;
    }

    .stButton > button:hover {
        border-color: #9CA3AF;
        background-color: #F9FAFB;
    }

    /* 채팅 입력창 */
    .stChatInput {
        padding-bottom: 20px;
    }

    /* 사이드바 */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 제목
# ============================================================

st.markdown(
    '<div class="main-title">⚾ KBO Baseball</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sub-title">'
    '야구가 처음이어도 괜찮아요.<br>'
    'KBO 야구의 규칙과 개념을 쉽게 알려드릴게요.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# 사이드바
# ============================================================

with st.sidebar:

    st.title("⚾ KBO Baseball")

    st.write(
        "야구 규칙과 용어가 궁금할 때 "
        "편하게 질문해보세요."
    )

    st.divider()

    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("현재 버전")
    st.caption("KBO 야구 학습 챗봇")


# ============================================================
# API Key
# ============================================================

openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-...",
)

if not openai_api_key:

    st.info(
        "OpenAI API Key를 입력하면 KBO 야구 도우미를 사용할 수 있습니다.",
        icon="🔑",
    )

    st.markdown(
        """
        ### 📚 이런 질문을 해보세요

        **⚾ 야구 규칙**
        - 스트라이크와 볼의 차이는?
        - 포스 아웃과 태그 아웃은 뭐가 달라?
        - 이닝은 어떻게 구성돼?

        **📊 야구 기록**
        - 타율이 뭐야?
        - OPS가 높으면 좋은 선수야?
        - ERA와 WHIP은 어떻게 달라?

        **🧠 야구 용어**
        - 병살이 뭐야?
        - 희생플라이가 뭐야?
        - 야수선택이 뭐야?

        **🎯 경기 상황**
        - 왜 이 상황에서 병살이 된 거야?
        - 주자가 왜 태그업을 해야 해?
        - 왜 투수가 교체된 거야?
        """
    )

    st.stop()


# ============================================================
# OpenAI Client
# ============================================================

client = OpenAI(api_key=openai_api_key)


# ============================================================
# 시스템 프롬프트
# ============================================================

system_prompt = """
당신은 KBO 야구를 처음 접하는 사람을 위한
친절한 '야구 학습 도우미'입니다.

사용자는 야구 초보자일 수 있습니다.
따라서 어려운 야구 용어를 사용할 때는 반드시
쉽게 풀어서 설명해주세요.


[기본 역할]

당신의 주요 역할은 다음과 같습니다.

1. 야구 규칙 설명
2. 야구 용어 설명
3. 야구 기록과 지표 설명
4. 경기 상황 분석
5. 사용자가 야구를 이해할 수 있도록 개념 간 관계 설명


[답변 방식]

가능하면 다음 순서로 설명해주세요.

① 한 줄 정의
② 쉽게 풀어서 설명
③ 실제 경기 상황 예시
④ 왜 그런 규칙이나 개념이 필요한지 설명
⑤ 비슷한 개념과 비교


예를 들어 사용자가
"병살이 뭐야?"라고 질문한다면,

단순히
"병살은 두 명을 아웃시키는 것입니다."

라고 끝내지 말고,

- 병살의 정의
- 주자가 1루에 있을 때 왜 병살이 가능한지
- 실제 땅볼 상황
- 2루에서 주자를 아웃시키고 1루에서 타자를 아웃시키는 과정
- 6-4-3 병살이 무엇인지

등을 초보자가 이해하기 쉽게 설명해주세요.


[초보자 배려]

사용자가 잘못 이해하고 있는 경우
"틀렸습니다"라고 단정적으로 말하기보다는
"거의 맞아요. 다만 한 가지 중요한 차이가 있어요."
처럼 부드럽게 설명해주세요.


[비교 설명]

비슷한 개념을 혼동할 수 있는 경우에는
표를 사용해서 차이를 설명해주세요.

예:

| 개념 | 의미 |
|---|---|
| 포스 아웃 | 주자가 반드시 다음 베이스로 가야 하는 상황에서의 아웃 |
| 태그 아웃 | 수비수가 공을 가진 글러브 등으로 주자를 직접 터치하는 아웃 |


[야구 기록]

타율, 출루율, 장타율, OPS, ERA, WHIP 등의 기록을 설명할 때는
단순히 공식만 제시하지 말고
"이 숫자가 높거나 낮다는 것이 실제 경기에서 무엇을 의미하는지"
설명해주세요.


[경기 상황]

사용자가 특정 경기 상황을 설명하면
상황을 단계별로 분석해주세요.

예:

상황
→ 주자 위치
→ 아웃 카운트
→ 타구
→ 수비 행동
→ 주자 행동
→ 결과

의 순서로 분석해주세요.


[KBO]

KBO 관련 질문에서는 KBO 리그의 맥락을 우선해서 설명해주세요.

다른 리그와 규칙이 다를 가능성이 있는 경우에는
KBO 기준인지 다른 리그 기준인지 구분해서 설명해주세요.


[정확성]

확실하지 않은 내용은 추측하지 마세요.

특히 최신 시즌의 선수 기록이나 경기 결과,
현재 규정 등 실시간 정보가 필요한 질문에 대해서는
현재 정보를 확인할 수 없다는 점을 명확히 알려주세요.


[말투]

친절하고 편안한 말투를 사용해주세요.

야구를 잘 모르는 사람이 질문해도
부끄럽지 않게 느끼도록 설명해주세요.

전문가처럼 어려운 말을 하기보다는
"야구를 같이 보면서 알려주는 친구"처럼 설명해주세요.
"""


# ============================================================
# Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# 카테고리
# ============================================================

st.markdown(
    '<div class="question-guide">'
    '<strong>📚 무엇이 궁금한가요?</strong><br>'
    '<span style="color:#6B7280;">'
    '아래 질문을 눌러 바로 시작하거나 자유롭게 질문해보세요.'
    '</span>'
    '</div>',
    unsafe_allow_html=True,
)


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        """
        <div class="category-card">
            <div class="category-title">⚾ 야구 규칙</div>
            <div class="category-description">
                스트라이크, 볼, 아웃, 이닝부터
                포스 아웃과 태그 아웃까지
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "스트라이크와 볼은 뭐가 달라?",
        key="rule_question",
    ):
        st.session_state.selected_question = (
            "야구에서 스트라이크와 볼은 정확히 뭐가 다른지 "
            "야구 초보자도 이해할 수 있게 설명해줘."
        )


with col2:

    st.markdown(
        """
        <div class="category-card">
            <div class="category-title">📊 야구 기록</div>
            <div class="category-description">
                타율, 출루율, OPS, ERA, WHIP 등
                선수 기록을 쉽게 이해하기
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "OPS가 높으면 좋은 선수야?",
        key="stat_question",
    ):
        st.session_state.selected_question = (
            "야구에서 OPS가 무엇인지 설명하고, "
            "OPS가 높다는 것이 실제 경기에서 어떤 의미인지 "
            "야구 초보자에게 쉽게 설명해줘."
        )


col3, col4 = st.columns(2)


with col3:

    st.markdown(
        """
        <div class="category-card">
            <div class="category-title">🧠 야구 용어</div>
            <div class="category-description">
                병살, 희생플라이, 도루, 야수선택 등
                경기에서 자주 듣는 용어
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "병살이 뭐야?",
        key="term_question",
    ):
        st.session_state.selected_question = (
            "야구에서 병살이 무엇인지 설명해줘. "
            "주자가 1루에 있고 타자가 땅볼을 쳤을 때를 "
            "예로 들어서 설명해줘."
        )


with col4:

    st.markdown(
        """
        <div class="category-card">
            <div class="category-title">🎯 경기 상황</div>
            <div class="category-description">
                특정 상황에서 왜 아웃인지,
                왜 점수가 인정되는지 등을 분석
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "포스 아웃과 태그 아웃의 차이는?",
        key="situation_question",
    ):
        st.session_state.selected_question = (
            "포스 아웃과 태그 아웃의 차이를 "
            "실제 경기 상황을 예로 들어서 설명해줘."
        )


# ============================================================
# 선택된 질문 처리
# ============================================================

if "selected_question" in st.session_state:

    prompt = st.session_state.selected_question

    del st.session_state.selected_question

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        response = st.write_stream(
            client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    *[
                        {
                            "role": message["role"],
                            "content": message["content"],
                        }
                        for message in st.session_state.messages
                    ],
                ],
                stream=True,
            )
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )


# ============================================================
# 기존 대화 표시
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# 사용자 질문
# ============================================================

if prompt := st.chat_input(
    "⚾ 야구에 대해 궁금한 것을 물어보세요..."
):

    # 사용자 질문 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # 사용자 질문 표시
    with st.chat_message("user"):
        st.markdown(prompt)

    # GPT 답변 생성
    with st.chat_message("assistant"):

        response = st.write_stream(
            client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    *[
                        {
                            "role": message["role"],
                            "content": message["content"],
                        }
                        for message in st.session_state.messages
                    ],
                ],
                stream=True,
            )
        )

    # 답변 저장
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
```
