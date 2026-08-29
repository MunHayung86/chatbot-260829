import streamlit as st
from openai import OpenAI


# ============================================================
# 1. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="KBO Baseball Learning",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background: #F5F5F3;
        color: #111111;
    }

    .block-container {
        max-width: 1160px;
        padding-top: 42px;
        padding-bottom: 80px;
    }

    header {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    * {
        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Pretendard",
            "Noto Sans KR",
            "Apple SD Gothic Neo",
            "Segoe UI",
            sans-serif;
    }


    /* =========================
       TOP BRAND
       ========================= */

    .brand-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }

    .brand-name {
        font-size: 15px;
        font-weight: 900;
        letter-spacing: 0.08em;
    }

    .brand-dot {
        display: inline-block;
        width: 9px;
        height: 9px;
        margin-right: 8px;
        border-radius: 50%;
        background: #FF5722;
    }

    .brand-meta {
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.12em;
        color: #999999;
    }


    /* =========================
       HERO
       ========================= */

    .hero-box {
        position: relative;
        overflow: hidden;
        min-height: 350px;
        padding: 48px 52px;
        margin-bottom: 44px;
        border-radius: 24px;
        background: #111111;
        box-sizing: border-box;
    }

    .hero-kicker {
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.16em;
        color: #FF5722;
        margin-bottom: 22px;
    }

    .hero-title {
        color: #FFFFFF;
        font-size: clamp(46px, 6vw, 76px);
        line-height: 0.98;
        font-weight: 950;
        letter-spacing: -0.065em;
    }

    .hero-orange {
        color: #FF5722;
    }

    .hero-description {
        margin-top: 25px;
        max-width: 520px;
        color: #A7A7A7;
        font-size: 14px;
        line-height: 1.75;
    }

    .hero-year {
        position: absolute;
        right: 45px;
        bottom: 24px;
        color: rgba(255,255,255,0.07);
        font-size: 120px;
        font-weight: 950;
        letter-spacing: -0.08em;
    }

    .hero-circle {
        position: absolute;
        width: 360px;
        height: 360px;
        right: -90px;
        top: -100px;
        border: 1px solid rgba(255,87,34,0.3);
        border-radius: 50%;
    }

    .hero-circle-small {
        position: absolute;
        width: 230px;
        height: 230px;
        right: 5px;
        top: -35px;
        border: 1px dashed rgba(255,87,34,0.5);
        border-radius: 50%;
    }


    /* =========================
       SECTION
       ========================= */

    .section-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 17px;
    }

    .section-label {
        margin-bottom: 6px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.15em;
        color: #FF5722;
    }

    .section-title {
        font-size: 25px;
        font-weight: 900;
        letter-spacing: -0.05em;
        color: #111111;
    }

    .section-count {
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.1em;
        color: #999999;
    }


    /* =========================
       STREAMLIT BUTTON
       ========================= */

    div.stButton > button {
        width: 100%;
        min-height: 155px;
        padding: 24px;
        border: 1px solid #DDDDD9;
        border-radius: 18px;
        background: #FFFFFF;
        color: #111111;
        text-align: left;
        white-space: pre-wrap;
        box-shadow: none;
        transition:
            transform 0.15s ease,
            border-color 0.15s ease,
            box-shadow 0.15s ease;
    }

    div.stButton > button:hover {
        border-color: #111111;
        background: #FFFFFF;
        color: #111111;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.07);
    }

    div.stButton > button p {
        font-size: 14px;
        line-height: 1.7;
    }


    /* =========================
       API KEY
       ========================= */

    .api-label {
        margin-top: 6px;
        margin-bottom: 7px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.14em;
        color: #888888;
    }

    .api-description {
        margin-bottom: 9px;
        font-size: 12px;
        color: #999999;
    }

    div[data-testid="stTextInput"] input {
        border: 1px solid #DDDDD9;
        border-radius: 11px;
        background: #FFFFFF;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #FF5722;
        box-shadow: 0 0 0 1px #FF5722;
    }


    /* =========================
       POPULAR QUESTIONS
       ========================= */

    .question-box {
        margin-top: 35px;
        padding: 27px 28px;
        border-radius: 20px;
        background: #111111;
    }

    .question-title {
        margin-bottom: 18px;
        color: #FFFFFF;
        font-size: 22px;
        font-weight: 900;
        letter-spacing: -0.04em;
    }

    .question-label {
        margin-bottom: 6px;
        color: #FF5722;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.15em;
    }

    .question-box div.stButton > button {
        min-height: 58px;
        padding: 14px 17px;
        border: 1px solid #303030;
        border-radius: 10px;
        background: #1B1B1B;
        color: #EEEEEE;
    }

    .question-box div.stButton > button:hover {
        border-color: #FF5722;
        background: #1B1B1B;
        color: #FFFFFF;
        transform: none;
        box-shadow: none;
    }


    /* =========================
       CHAT
       ========================= */

    .chat-header {
        margin-top: 38px;
        margin-bottom: 18px;
        padding-top: 28px;
        border-top: 1px solid #DDDDD9;
    }

    .chat-label {
        margin-bottom: 6px;
        color: #FF5722;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.15em;
    }

    .chat-title {
        color: #111111;
        font-size: 25px;
        font-weight: 900;
        letter-spacing: -0.05em;
    }

    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    [data-testid="stChatMessageContent"] {
        font-size: 15px;
        line-height: 1.8;
    }

    [data-testid="stChatInput"] textarea {
        border: 1px solid #DDDDD9;
        border-radius: 13px;
        background: #FFFFFF;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: #FF5722;
        box-shadow: 0 0 0 1px #FF5722;
    }


    /* =========================
       FOOTER
       ========================= */

    .footer-line {
        height: 1px;
        margin-top: 60px;
        margin-bottom: 15px;
        background: #DDDDD9;
    }

    .footer-text {
        color: #999999;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 0.1em;
    }


    /* =========================
       MOBILE
       ========================= */

    @media (max-width: 768px) {

        .block-container {
            padding: 25px 18px 60px 18px;
        }

        .brand-meta {
            display: none;
        }

        .hero-box {
            min-height: 390px;
            padding: 35px 28px;
            border-radius: 18px;
        }

        .hero-title {
            font-size: 48px;
        }

        .hero-description {
            max-width: 300px;
        }

        .hero-year {
            font-size: 80px;
            right: 20px;
        }

        .hero-circle {
            width: 280px;
            height: 280px;
        }

        .hero-circle-small {
            width: 180px;
            height: 180px;
        }

        .section-title {
            font-size: 21px;
        }

        div.stButton > button {
            min-height: 145px;
        }

        .question-box {
            padding: 22px 18px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_question" not in st.session_state:
    st.session_state.selected_question = None


# ============================================================
# 4. TOP BRAND
# ============================================================

st.markdown(
    """
    <div class="brand-row">
        <div class="brand-name">
            <span class="brand-dot"></span>
            KBO BASEBALL
        </div>

        <div class="brand-meta">
            AI BASEBALL LEARNING
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 5. HERO
# ============================================================

st.markdown(
    """
    <div class="hero-box">

        <div class="hero-kicker">
            KBO BASEBALL LEARNING
        </div>

        <div class="hero-title">
            야구를 보다,<br>
            <span class="hero-orange">이해하다.</span>
        </div>

        <div class="hero-description">
            야구가 처음이어도 괜찮아요.<br>
            KBO의 규칙, 용어, 기록과 경기 상황을<br>
            AI와 함께 하나씩 배워보세요.
        </div>

        <div class="hero-year">
            26
        </div>

        <div class="hero-circle"></div>
        <div class="hero-circle-small"></div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 6. API KEY
# ============================================================

st.markdown(
    '<div class="api-label">OPENAI API KEY</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="api-description">API Key를 입력하면 야구 학습 챗봇을 사용할 수 있습니다.</div>',
    unsafe_allow_html=True,
)

openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-...",
    label_visibility="collapsed",
)


# ============================================================
# 7. API KEY가 없을 때
# ============================================================

if not openai_api_key:

    st.markdown(
        """
        <div class="section-row">
            <div>
                <div class="section-label">START HERE</div>
                <div class="section-title">무엇부터 배워볼까요?</div>
            </div>

            <div class="section-count">
                04 CATEGORIES
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "01 / RULE\n\n야구 규칙\n\n스트라이크, 볼, 아웃부터 포스 아웃과 태그 아웃까지",
            disabled=True,
            key="rule_disabled",
        )

    with col2:
        st.button(
            "02 / TERM\n\n야구 용어\n\n병살, 희생플라이, 도루 등 경기에서 자주 듣는 용어",
            disabled=True,
            key="term_disabled",
        )

    col3, col4 = st.columns(2)

    with col3:
        st.button(
            "03 / STATS\n\n야구 기록\n\n타율, 출루율, 장타율, OPS, ERA, WHIP 이해하기",
            disabled=True,
            key="stats_disabled",
        )

    with col4:
        st.button(
            "04 / SITUATION\n\n경기 상황\n\n실제 경기 장면을 통해 플레이의 결과 이해하기",
            disabled=True,
            key="situation_disabled",
        )

    st.markdown(
        """
        <div class="question-box">

            <div class="question-label">
                POPULAR QUESTIONS
            </div>

            <div class="question-title">
                API Key를 입력하고 시작해보세요.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.stop()


# ============================================================
# 8. OPENAI CLIENT
# ============================================================

client = OpenAI(
    api_key=openai_api_key
)


# ============================================================
# 9. SYSTEM PROMPT
# ============================================================

system_prompt = """
당신은 KBO 야구를 처음 접하는 사람을 위한
친절한 야구 학습 도우미입니다.

사용자는 야구 초보자일 수 있습니다.
전문적인 야구 용어를 사용할 경우 반드시
쉬운 말로 풀어서 설명해주세요.

주요 영역은 다음 네 가지입니다.

1. 야구 규칙
2. 야구 용어
3. 야구 기록
4. 경기 상황

개념을 설명할 때 가능하면 다음 순서로 설명합니다.

① 한 줄 정의
② 쉽게 풀어서 설명
③ 실제 경기 상황 예시
④ 경기에서 왜 중요한지 설명
⑤ 비슷한 개념과 비교

단순한 사전식 정의로 끝내지 말고
사용자가 실제 KBO 경기를 볼 때
이해할 수 있도록 설명해주세요.

야구 초보자가 이해하기 어려운 전문 용어를
연속해서 사용하지 마세요.

사용자가 잘못 이해하고 있다면
부드럽게 교정해주세요.

야구 규칙에서는
스트라이크, 볼, 아웃, 이닝,
포스 아웃, 태그 아웃, 병살,
희생플라이, 희생번트, 도루,
인필드 플라이, 야수선택 등을
실제 경기 상황과 연결해서 설명합니다.

야구 기록에서는
타율, 출루율, 장타율, OPS,
ERA, WHIP, 승리, 세이브 등의 기록을
공식만 설명하지 말고
그 숫자가 실제 경기에서 무엇을 의미하는지
설명해주세요.

경기 상황 질문을 받으면 다음 순서로 분석합니다.

상황
→ 주자 위치
→ 아웃 카운트
→ 타구
→ 수비 행동
→ 주자 행동
→ 결과

KBO 리그 관련 질문에서는
KBO 리그의 맥락을 우선해서 설명해주세요.

현재 시즌 선수 기록,
오늘 경기 결과,
현재 순위 등 실시간 정보가 필요한 경우
최신 데이터가 제공되지 않았다면 추측하지 마세요.

친절하고 차분하게,
야구를 같이 보면서 알려주는 친구처럼 설명해주세요.
"""


# ============================================================
# 10. RESPONSE FUNCTION
# ============================================================

def get_response():

    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            *st.session_state.messages,
        ],
        stream=True,
    )


# ============================================================
# 11. STARTER QUESTIONS
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="section-row">
            <div>
                <div class="section-label">START WITH A QUESTION</div>
                <div class="section-title">궁금한 것부터 시작하세요.</div>
            </div>

            <div class="section-count">
                BEGINNER
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "스트라이크와 볼은 뭐가 달라?",
            key="starter_strike",
        ):
            st.session_state.selected_question = (
                "스트라이크와 볼은 무엇이 다른지 "
                "야구를 처음 보는 사람도 이해할 수 있게 설명해줘."
            )
            st.rerun()

        if st.button(
            "병살은 어떻게 만들어져?",
            key="starter_double_play",
        ):
            st.session_state.selected_question = (
                "야구에서 병살이 무엇인지 설명해줘. "
                "1루에 주자가 있고 타자가 땅볼을 쳤을 때를 예로 들어줘."
            )
            st.rerun()

    with col2:

        if st.button(
            "OPS가 높으면 좋은 선수야?",
            key="starter_ops",
        ):
            st.session_state.selected_question = (
                "OPS가 무엇인지 설명해줘. "
                "OPS가 높다는 것이 타자에게 어떤 의미인지 "
                "실제 야구를 볼 때 이해할 수 있도록 설명해줘."
            )
            st.rerun()

        if st.button(
            "포스 아웃과 태그 아웃의 차이는?",
            key="starter_out",
        ):
            st.session_state.selected_question = (
                "포스 아웃과 태그 아웃의 차이를 "
                "실제 경기 상황을 예로 들어서 쉽게 설명해줘."
            )
            st.rerun()


# ============================================================
# 12. SELECTED STARTER QUESTION
# ============================================================

if st.session_state.selected_question:

    question = st.session_state.selected_question

    st.session_state.selected_question = None

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        response = st.write_stream(
            get_response()
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    st.rerun()


# ============================================================
# 13. EXISTING CONVERSATION
# ============================================================

if st.session_state.messages:

    st.markdown(
        """
        <div class="chat-header">
            <div class="chat-label">
                CONVERSATION
            </div>

            <div class="chat-title">
                야구를 함께 알아볼게요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# ============================================================
# 14. FREE CHAT
# ============================================================

prompt = st.chat_input(
    "야구에 대해 궁금한 것을 물어보세요..."
)

if prompt:

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
            get_response()
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )


# ============================================================
# 15. FOOTER
# ============================================================

st.markdown(
    '<div class="footer-line"></div>',
    unsafe_allow_html=True,
)

footer_left, footer_right = st.columns(2)

with footer_left:
    st.markdown(
        '<div class="footer-text">KBO BASEBALL LEARNING</div>',
        unsafe_allow_html=True,
    )

with footer_right:
    st.markdown(
        '<div class="footer-text" style="text-align:right;">RULE · TERM · STATS · SITUATION</div>',
        unsafe_allow_html=True,
    )
