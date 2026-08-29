import streamlit as st
from openai import OpenAI


# ============================================================
# 1. 페이지 설정
# ============================================================

st.set_page_config(
    page_title="KBO Baseball",
    page_icon="⚾",
    layout="centered",
)


# ============================================================
# 2. 디자인
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       전체 페이지
    -------------------------------------------------------- */

    .stApp {
        background-color: #F6F6F4;
        color: #171717;
    }

    .block-container {
        max-width: 920px;
        padding-top: 3.5rem;
        padding-bottom: 7rem;
    }


    /* --------------------------------------------------------
       Streamlit 기본 요소 숨기기
    -------------------------------------------------------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }


    /* --------------------------------------------------------
       메인 헤더
    -------------------------------------------------------- */

    .hero {
        position: relative;
        padding: 10px 0 34px 0;
    }

    .hero-label {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.16em;
        color: #17365D;
        margin-bottom: 13px;
    }

    .hero-title {
        font-size: 48px;
        line-height: 1.05;
        font-weight: 850;
        letter-spacing: -0.045em;
        color: #111111;
        margin: 0;
    }

    .hero-title span {
        color: #17365D;
    }

    .hero-description {
        margin-top: 15px;
        font-size: 16px;
        line-height: 1.7;
        color: #737373;
    }


    /* --------------------------------------------------------
       야구공 스티치 장식
    -------------------------------------------------------- */

    .baseball-line {
        width: 100%;
        height: 1px;
        background: #D9D9D6;
        position: relative;
        margin: 5px 0 30px 0;
    }

    .baseball-line::before {
        content: "";
        position: absolute;
        left: 0;
        top: -4px;
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #17365D;
    }


    /* --------------------------------------------------------
       Section 제목
    -------------------------------------------------------- */

    .section-label {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.15em;
        color: #888888;
        margin-bottom: 13px;
        text-transform: uppercase;
    }


    /* --------------------------------------------------------
       카테고리 카드
    -------------------------------------------------------- */

    .category-card {
        background: #FFFFFF;
        border: 1px solid #E3E3E0;
        border-radius: 14px;
        padding: 22px 22px 20px 22px;
        min-height: 125px;
        transition: 0.2s ease;
        margin-bottom: 10px;
    }

    .category-card:hover {
        border-color: #17365D;
    }

    .category-number {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.1em;
        color: #17365D;
        margin-bottom: 9px;
    }

    .category-title {
        font-size: 19px;
        font-weight: 750;
        color: #171717;
        margin-bottom: 7px;
    }

    .category-description {
        font-size: 13px;
        line-height: 1.55;
        color: #777777;
    }


    /* --------------------------------------------------------
       추천 질문 영역
    -------------------------------------------------------- */

    .question-section {
        margin-top: 30px;
    }

    .question-box {
        background: #FFFFFF;
        border: 1px solid #E3E3E0;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 9px;
    }

    .question-label {
        font-size: 12px;
        color: #17365D;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .question-text {
        font-size: 15px;
        color: #222222;
        line-height: 1.5;
    }


    /* --------------------------------------------------------
       버튼
    -------------------------------------------------------- */

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #E1E1DE;
        background-color: #FFFFFF;
        color: #252525;
        min-height: 42px;
        font-size: 13px;
        font-weight: 600;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #17365D;
        color: #17365D;
        background-color: #FAFBFC;
    }


    /* --------------------------------------------------------
       API Key 영역
    -------------------------------------------------------- */

    .api-title {
        font-size: 12px;
        font-weight: 750;
        color: #555555;
        margin-bottom: 5px;
    }


    /* --------------------------------------------------------
       Chat UI
    -------------------------------------------------------- */

    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
        padding-left: 0;
        padding-right: 0;
    }

    [data-testid="stChatMessageContent"] {
        font-size: 15px;
        line-height: 1.75;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: transparent;
    }


    /* --------------------------------------------------------
       Chat input
    -------------------------------------------------------- */

    [data-testid="stChatInput"] {
        border-top: 1px solid #DDDDD9;
        background-color: #F6F6F4;
        padding-top: 15px;
    }

    [data-testid="stChatInput"] textarea {
        border: 1px solid #D9D9D6;
        border-radius: 13px;
        background: #FFFFFF;
    }


    /* --------------------------------------------------------
       API 안내
    -------------------------------------------------------- */

    .api-info {
        background: #FFFFFF;
        border: 1px solid #E3E3E0;
        border-radius: 12px;
        padding: 17px 19px;
        margin-top: 10px;
        margin-bottom: 25px;
        font-size: 13px;
        color: #777777;
        line-height: 1.6;
    }

    .api-info strong {
        color: #333333;
    }


    /* --------------------------------------------------------
       Footer
    -------------------------------------------------------- */

    .footer {
        text-align: center;
        color: #AAAAAA;
        font-size: 11px;
        margin-top: 55px;
        padding-top: 20px;
        border-top: 1px solid #E0E0DD;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. Hero
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-label">
            KBO BASEBALL LEARNING
        </div>

        <div class="hero-title">
            야구를 보다,<br>
            <span>이해하다.</span>
        </div>

        <div class="hero-description">
            야구가 처음이어도 괜찮아요.<br>
            KBO의 규칙과 용어, 기록을 경기 상황과 함께 쉽게 배워보세요.
        </div>

    </div>

    <div class="baseball-line"></div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. API Key 입력
# ============================================================

st.markdown(
    '<div class="api-title">OPENAI API KEY</div>',
    unsafe_allow_html=True,
)

openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-...",
    label_visibility="collapsed",
)

if not openai_api_key:

    st.markdown(
        """
        <div class="api-info">
            <strong>챗봇을 시작하려면 API Key가 필요합니다.</strong><br>
            OpenAI API Key를 입력하면 야구 학습 도우미를 사용할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 5. Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# 6. API Key가 없으면 여기서 종료
# ============================================================

if not openai_api_key:

    st.markdown(
        """
        <div class="section-label">
            START HERE
        </div>

        <div class="question-box">
            <div class="question-label">01 · RULE</div>
            <div class="question-text">
                스트라이크와 볼은 뭐가 달라?
            </div>
        </div>

        <div class="question-box">
            <div class="question-label">02 · TERM</div>
            <div class="question-text">
                병살은 어떻게 만들어져?
            </div>
        </div>

        <div class="question-box">
            <div class="question-label">03 · STATS</div>
            <div class="question-text">
                OPS가 높으면 좋은 선수야?
            </div>
        </div>

        <div class="question-box">
            <div class="question-label">04 · SITUATION</div>
            <div class="question-text">
                포스 아웃과 태그 아웃은 뭐가 달라?
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="footer">
            KBO BASEBALL LEARNING · AI Baseball Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.stop()


# ============================================================
# 7. OpenAI Client
# ============================================================

client = OpenAI(
    api_key=openai_api_key
)


# ============================================================
# 8. System Prompt
# ============================================================

system_prompt = """
당신은 KBO 야구를 처음 접하는 사람을 위한
친절한 야구 학습 도우미입니다.

사용자는 야구 초보자일 수 있습니다.
따라서 전문적인 야구 용어를 사용할 때는
반드시 쉬운 말로 풀어서 설명해주세요.


[핵심 역할]

다음 네 가지 영역을 중심으로 설명합니다.

1. 야구 규칙
2. 야구 용어
3. 야구 기록
4. 경기 상황


[답변 원칙]

사용자가 개념을 질문하면 가능하면 다음 순서로 설명해주세요.

① 한 줄 정의
② 쉽게 풀어서 설명
③ 실제 경기 상황 예시
④ 경기에서 왜 중요한지 설명
⑤ 비슷한 개념과 비교


[야구 초보자]

야구를 처음 보는 사람도 이해할 수 있도록 설명해주세요.

전문 용어를 연속해서 사용하지 말고,
필요한 경우 용어를 먼저 정의해주세요.

사용자가 잘못 이해하고 있다면
부드럽게 교정해주세요.


[규칙]

스트라이크, 볼, 아웃, 이닝,
포스 아웃, 태그 아웃, 병살,
희생플라이, 희생번트, 도루,
인필드 플라이, 야수선택 등의 규칙을
실제 경기 상황과 연결해서 설명해주세요.


[기록]

타율, 출루율, 장타율, OPS,
ERA, WHIP, 승리, 세이브 등의 기록을
단순히 공식만 알려주지 말고
그 기록이 실제로 무엇을 의미하는지 설명해주세요.

필요하다면 표를 활용해서
비슷한 기록을 비교해주세요.


[경기 상황 분석]

사용자가 경기 상황을 설명하면 다음 순서로 분석해주세요.

상황
→ 주자 위치
→ 아웃 카운트
→ 타구
→ 수비 행동
→ 주자 행동
→ 결과

그리고 왜 그런 결과가 발생했는지 설명해주세요.


[KBO]

KBO 리그와 관련된 질문에서는
KBO 리그의 맥락을 우선적으로 고려해주세요.

KBO와 다른 리그의 규칙이 다를 수 있다면
어느 리그 기준인지 구분해서 설명해주세요.


[최신 정보]

현재 시즌의 선수 기록,
오늘 경기 결과,
현재 순위,
최신 규정 등 실시간 정보가 필요한 질문은
확인할 수 있는 최신 데이터가 제공되지 않았다면
추측하지 마세요.

확실하지 않은 정보는
확실하지 않다고 알려주세요.


[말투]

친절하고 차분하게 설명해주세요.

야구를 잘 모르는 사람이
질문하는 것을 전혀 부끄럽게 생각하지 않도록
편안한 분위기를 만들어주세요.

단순한 사전식 설명보다
"실제 야구 경기를 같이 보면서 알려주는 것처럼"
설명해주세요.
"""


# ============================================================
# 9. GPT 호출 함수
# ============================================================

def generate_response():

    return client.chat.completions.create(
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


# ============================================================
# 10. 기존 대화 표시
# ============================================================

if st.session_state.messages:

    st.markdown(
        """
        <div class="section-label">
            CONVERSATION
        </div>
        """,
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# ============================================================
# 11. 첫 화면 추천 질문
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="question-section">

            <div class="section-label">
                START WITH A QUESTION
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⚾ 스트라이크와 볼은 뭐가 달라?",
            key="question_rule",
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": (
                        "야구에서 스트라이크와 볼은 "
                        "정확히 무엇이 다른지 야구 초보자에게 "
                        "쉽게 설명해줘."
                    ),
                }
            )

            st.rerun()

    with col2:

        if st.button(
            "🧠 병살은 어떻게 만들어져?",
            key="question_double_play",
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": (
                        "야구에서 병살이 무엇인지 설명해줘. "
                        "1루에 주자가 있는 상황에서 타자가 "
                        "땅볼을 쳤을 때를 예로 들어줘."
                    ),
                }
            )

            st.rerun()

    col3, col4 = st.columns(2)

    with col3:

        if st.button(
            "📊 OPS가 높으면 좋은 선수야?",
            key="question_ops",
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": (
                        "야구에서 OPS가 무엇인지 설명해줘. "
                        "OPS가 높다는 것이 실제 경기에서 "
                        "어떤 의미인지 야구 초보자에게 알려줘."
                    ),
                }
            )

            st.rerun()

    with col4:

        if st.button(
            "🎯 포스 아웃과 태그 아웃의 차이는?",
            key="question_out",
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": (
                        "포스 아웃과 태그 아웃의 차이를 "
                        "실제 경기 상황을 예로 들어서 설명해줘."
                    ),
                }
            )

            st.rerun()


# ============================================================
# 12. 추천 질문으로 들어온 경우 GPT 답변 생성
# ============================================================

if (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
):

    # 마지막 메시지가 아직 답변되지 않은 경우에만 실행
    if (
        "last_answered_index" not in st.session_state
        or st.session_state.last_answered_index
        != len(st.session_state.messages) - 1
    ):

        with st.chat_message("assistant"):

            response = st.write_stream(
                generate_response()
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        st.session_state.last_answered_index = (
            len(st.session_state.messages) - 1
        )


# ============================================================
# 13. 사용자 자유 질문
# ============================================================

if prompt := st.chat_input(
    "야구에 대해 궁금한 것을 물어보세요..."
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

    # GPT 답변
    with st.chat_message("assistant"):

        response = st.write_stream(
            generate_response()
        )

    # 답변 저장
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    st.session_state.last_answered_index = (
        len(st.session_state.messages) - 1
    )


# ============================================================
# 14. Footer
# ============================================================

st.markdown(
    """
    <div class="footer">
        KBO BASEBALL LEARNING · AI Baseball Assistant
    </div>
    """,
    unsafe_allow_html=True,
)
