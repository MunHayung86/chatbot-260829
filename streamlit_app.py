import streamlit as st
from openai import OpenAI
from textwrap import dedent


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
    dedent(
        """
        <style>

        /* ====================================================
           GLOBAL
        ==================================================== */

        .stApp {
            background: #F4F4F2;
            color: #111111;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 48px;
            padding-bottom: 80px;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }


        /* ====================================================
           TYPOGRAPHY
        ==================================================== */

        * {
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Pretendard",
                "Noto Sans KR",
                "Segoe UI",
                sans-serif;
        }


        /* ====================================================
           TOP BRAND
        ==================================================== */

        .top-brand {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 22px;
        }

        .brand-left {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .brand-mark {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #111111;
            position: relative;
        }

        .brand-mark::before {
            content: "";
            position: absolute;
            width: 13px;
            height: 23px;
            border-right: 2px dashed #FF5722;
            border-radius: 50%;
            top: 3px;
            left: 8px;
            transform: rotate(-22deg);
        }

        .brand-name {
            font-size: 14px;
            font-weight: 900;
            letter-spacing: 0.08em;
            color: #111111;
        }

        .brand-right {
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.12em;
            color: #888888;
        }


        /* ====================================================
           HERO
        ==================================================== */

        .hero {
            position: relative;
            overflow: hidden;
            background: #111111;
            min-height: 360px;
            border-radius: 24px;
            padding: 48px 52px;
            margin-bottom: 42px;
        }

        .hero::after {
            content: "";
            position: absolute;
            width: 390px;
            height: 390px;
            border: 1px solid rgba(255, 87, 34, 0.30);
            border-radius: 50%;
            right: -95px;
            top: -80px;
        }

        .hero::before {
            content: "";
            position: absolute;
            width: 260px;
            height: 260px;
            border: 1px dashed rgba(255, 87, 34, 0.50);
            border-radius: 50%;
            right: -20px;
            top: -20px;
        }

        .hero-content {
            position: relative;
            z-index: 2;
            max-width: 650px;
        }

        .hero-kicker {
            display: inline-flex;
            align-items: center;
            background: #FF5722;
            color: #FFFFFF;
            border-radius: 999px;
            padding: 8px 13px;
            font-size: 10px;
            font-weight: 900;
            letter-spacing: 0.12em;
            margin-bottom: 24px;
        }

        .hero-title {
            font-size: clamp(48px, 6vw, 78px);
            line-height: 0.98;
            font-weight: 950;
            letter-spacing: -0.065em;
            color: #FFFFFF;
            margin: 0;
        }

        .hero-title .orange {
            color: #FF5722;
        }

        .hero-description {
            margin-top: 25px;
            color: #A8A8A8;
            font-size: 15px;
            line-height: 1.7;
        }

        .hero-number {
            position: absolute;
            right: 46px;
            bottom: 30px;
            z-index: 2;
            color: rgba(255,255,255,0.08);
            font-size: 130px;
            line-height: 1;
            font-weight: 950;
            letter-spacing: -0.08em;
        }


        /* ====================================================
           SECTION HEADER
        ==================================================== */

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: end;
            margin-bottom: 15px;
        }

        .section-title {
            font-size: 22px;
            font-weight: 900;
            letter-spacing: -0.04em;
            color: #111111;
        }

        .section-label {
            font-size: 10px;
            font-weight: 900;
            letter-spacing: 0.14em;
            color: #999999;
            margin-bottom: 5px;
        }

        .section-count {
            font-size: 11px;
            font-weight: 700;
            color: #999999;
        }


        /* ====================================================
           CATEGORY CARDS
        ==================================================== */

        .category-card {
            position: relative;
            min-height: 180px;
            background: #FFFFFF;
            border: 1px solid #E1E1DE;
            border-radius: 18px;
            padding: 25px;
            margin-bottom: 14px;
            overflow: hidden;
            transition: all 0.2s ease;
        }

        .category-card:hover {
            border-color: #111111;
            transform: translateY(-2px);
        }

        .category-card::after {
            content: "";
            position: absolute;
            width: 90px;
            height: 90px;
            border: 1px solid #EEEEEB;
            border-radius: 50%;
            right: -30px;
            bottom: -30px;
        }

        .category-number {
            font-size: 10px;
            font-weight: 900;
            letter-spacing: 0.12em;
            color: #FF5722;
            margin-bottom: 28px;
        }

        .category-title {
            font-size: 22px;
            font-weight: 900;
            letter-spacing: -0.04em;
            color: #111111;
            margin-bottom: 7px;
        }

        .category-description {
            max-width: 300px;
            font-size: 13px;
            line-height: 1.6;
            color: #888888;
        }

        .category-arrow {
            position: absolute;
            right: 23px;
            top: 23px;
            font-size: 20px;
            color: #BBBBBB;
        }


        /* ====================================================
           QUESTIONS
        ==================================================== */

        .questions-wrapper {
            background: #111111;
            border-radius: 20px;
            padding: 27px;
            margin-top: 32px;
        }

        .questions-wrapper .section-label {
            color: #FF5722;
        }

        .questions-wrapper .section-title {
            color: #FFFFFF;
        }

        .question-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 17px 0;
            border-bottom: 1px solid #292929;
        }

        .question-item:last-child {
            border-bottom: none;
        }

        .question-text {
            color: #EEEEEE;
            font-size: 14px;
            font-weight: 600;
        }

        .question-arrow {
            color: #FF5722;
            font-size: 17px;
        }


        /* ====================================================
           STREAMLIT BUTTONS
        ==================================================== */

        .stButton {
            margin-top: -64px;
            position: relative;
            z-index: 5;
        }

        .stButton > button {
            width: 100%;
            min-height: 180px;
            border-radius: 18px;
            border: 1px solid transparent;
            background: transparent;
            color: transparent;
            box-shadow: none;
        }

        .stButton > button:hover {
            border: 1px solid #111111;
            background: rgba(255,255,255,0.02);
            color: transparent;
        }


        /* ====================================================
           API KEY
        ==================================================== */

        .api-section {
            background: #FFFFFF;
            border: 1px solid #E1E1DE;
            border-radius: 16px;
            padding: 20px 22px;
            margin-bottom: 35px;
        }

        .api-label {
            font-size: 10px;
            font-weight: 900;
            letter-spacing: 0.13em;
            color: #888888;
            margin-bottom: 8px;
        }

        .api-description {
            font-size: 12px;
            color: #999999;
            margin-bottom: 10px;
        }


        /* ====================================================
           CHAT
        ==================================================== */

        .chat-section {
            margin-top: 35px;
        }

        [data-testid="stChatMessage"] {
            background: transparent;
            border: none;
            padding: 12px 0;
        }

        [data-testid="stChatMessageContent"] {
            font-size: 15px;
            line-height: 1.8;
        }

        [data-testid="stChatInput"] {
            padding-top: 10px;
        }

        [data-testid="stChatInput"] textarea {
            border: 1px solid #D8D8D5;
            border-radius: 14px;
            background: #FFFFFF;
            font-size: 14px;
        }

        [data-testid="stChatInput"] textarea:focus {
            border-color: #FF5722;
            box-shadow: 0 0 0 1px #FF5722;
        }


        /* ====================================================
           FOOTER
        ==================================================== */

        .footer {
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid #DDDDD9;
            display: flex;
            justify-content: space-between;
            color: #AAAAAA;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.08em;
        }


        /* ====================================================
           MOBILE
        ==================================================== */

        @media (max-width: 768px) {

            .block-container {
                padding: 25px 18px 60px 18px;
            }

            .hero {
                min-height: 330px;
                padding: 32px 28px;
                border-radius: 18px;
            }

            .hero-title {
                font-size: 48px;
            }

            .hero-number {
                font-size: 90px;
                right: 20px;
            }

            .category-card {
                min-height: 155px;
            }

            .footer {
                flex-direction: column;
                gap: 8px;
            }
        }

        </style>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# 3. SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ============================================================
# 4. OPENAI API KEY
# ============================================================

st.markdown(
    dedent(
        """
        <div class="top-brand">
            <div class="brand-left">
                <div class="brand-mark"></div>
                <div class="brand-name">KBO BASEBALL</div>
            </div>

            <div class="brand-right">
                AI BASEBALL LEARNING
            </div>
        </div>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# 5. HERO
# ============================================================

st.markdown(
    dedent(
        """
        <div class="hero">

            <div class="hero-content">

                <div class="hero-kicker">
                    KBO BASEBALL LEARNING
                </div>

                <div class="hero-title">
                    야구를 보다,<br>
                    <span class="orange">이해하다.</span>
                </div>

                <div class="hero-description">
                    야구가 처음이어도 괜찮아요.<br>
                    KBO의 규칙, 용어, 기록과 경기 상황을
                    AI와 함께 하나씩 배워보세요.
                </div>

            </div>

            <div class="hero-number">
                09
            </div>

        </div>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# 6. API KEY AREA
# ============================================================

st.markdown(
    dedent(
        """
        <div class="api-section">
            <div class="api-label">OPENAI API KEY</div>
            <div class="api-description">
                API Key를 입력하면 야구 학습 챗봇을 사용할 수 있습니다.
            </div>
        </div>
        """
    ),
    unsafe_allow_html=True,
)

openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-...",
    label_visibility="collapsed",
)


# ============================================================
# 7. API KEY 없을 때
# ============================================================

if not openai_api_key:

    st.markdown(
        dedent(
            """
            <div class="section-header">
                <div>
                    <div class="section-label">START HERE</div>
                    <div class="section-title">무엇부터 배워볼까요?</div>
                </div>

                <div class="section-count">
                    04 CATEGORIES
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            dedent(
                """
                <div class="category-card">
                    <div class="category-number">01 / RULE</div>
                    <div class="category-title">야구 규칙</div>
                    <div class="category-description">
                        스트라이크와 볼부터 아웃, 이닝,
                        포스 아웃과 태그 아웃까지
                    </div>
                    <div class="category-arrow">↗</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            dedent(
                """
                <div class="category-card">
                    <div class="category-number">02 / TERM</div>
                    <div class="category-title">야구 용어</div>
                    <div class="category-description">
                        병살, 희생플라이, 도루, 야수선택 등
                        경기에서 자주 듣는 용어
                    </div>
                    <div class="category-arrow">↗</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    col3, col4 = st.columns(2)

    with col3:

        st.markdown(
            dedent(
                """
                <div class="category-card">
                    <div class="category-number">03 / STATS</div>
                    <div class="category-title">야구 기록</div>
                    <div class="category-description">
                        타율, 출루율, 장타율, OPS,
                        ERA, WHIP 등을 쉽게 이해하기
                    </div>
                    <div class="category-arrow">↗</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    with col4:

        st.markdown(
            dedent(
                """
                <div class="category-card">
                    <div class="category-number">04 / SITUATION</div>
                    <div class="category-title">경기 상황</div>
                    <div class="category-description">
                        실제 경기에서 왜 이런 결과가 나왔는지
                        상황별로 하나씩 분석하기
                    </div>
                    <div class="category-arrow">↗</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        dedent(
            """
            <div class="questions-wrapper">

                <div class="section-label">
                    POPULAR QUESTIONS
                </div>

                <div class="section-title">
                    이런 것부터 물어보세요.
                </div>

                <div class="question-item">
                    <div class="question-text">
                        스트라이크와 볼은 뭐가 달라?
                    </div>
                    <div class="question-arrow">→</div>
                </div>

                <div class="question-item">
                    <div class="question-text">
                        병살은 어떻게 만들어져?
                    </div>
                    <div class="question-arrow">→</div>
                </div>

                <div class="question-item">
                    <div class="question-text">
                        OPS가 높으면 좋은 선수야?
                    </div>
                    <div class="question-arrow">→</div>
                </div>

                <div class="question-item">
                    <div class="question-text">
                        포스 아웃과 태그 아웃의 차이는?
                    </div>
                    <div class="question-arrow">→</div>
                </div>

            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        dedent(
            """
            <div class="footer">
                <div>KBO BASEBALL LEARNING</div>
                <div>AI BASEBALL ASSISTANT</div>
            </div>
            """
        ),
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


[주요 역할]

다음 네 가지 영역을 중심으로 설명합니다.

1. 야구 규칙
2. 야구 용어
3. 야구 기록
4. 경기 상황


[답변 방식]

개념을 설명할 때 가능하면 다음 순서를 사용합니다.

① 한 줄 정의
② 쉽게 풀어서 설명
③ 실제 경기 상황 예시
④ 경기에서 왜 중요한지 설명
⑤ 비슷한 개념과 비교

단순한 사전식 정의로 끝내지 말고
사용자가 실제 야구 경기를 볼 때
이해할 수 있도록 설명해주세요.


[초보자 배려]

야구를 처음 보는 사람도 이해할 수 있도록
전문 용어를 연속해서 사용하지 마세요.

사용자가 잘못 이해하고 있다면
부드럽게 교정해주세요.

예:
"거의 맞아요. 다만 한 가지 중요한 차이가 있어요."
와 같은 방식으로 설명합니다.


[야구 규칙]

스트라이크, 볼, 아웃, 이닝,
포스 아웃, 태그 아웃, 병살,
희생플라이, 희생번트, 도루,
인필드 플라이, 야수선택 등을
실제 경기 상황과 연결해서 설명합니다.


[야구 기록]

타율, 출루율, 장타율, OPS,
ERA, WHIP, 승리, 세이브 등의 기록을
공식만 설명하지 말고
그 숫자가 실제 경기에서 무엇을 의미하는지
설명해주세요.

필요하다면 표를 사용해서
비슷한 기록을 비교해주세요.


[경기 상황 분석]

사용자가 경기 상황을 설명하면 다음 순서로 분석합니다.

상황
→ 주자 위치
→ 아웃 카운트
→ 타구
→ 수비 행동
→ 주자 행동
→ 결과

그리고 왜 그런 결과가 발생했는지 설명해주세요.


[KBO]

KBO 리그 관련 질문에서는
KBO 리그의 맥락을 우선해서 설명해주세요.

다른 리그와 규칙이 다를 수 있다면
어느 리그 기준인지 구분해서 설명해주세요.


[최신 정보]

현재 시즌 선수 기록,
오늘 경기 결과,
현재 순위,
최신 규정 등 실시간 정보가 필요한 경우
확인할 수 있는 최신 데이터가 제공되지 않았다면
추측하지 마세요.

확실하지 않은 정보는
확실하지 않다고 알려주세요.


[말투]

친절하고 차분하게 설명해주세요.

야구를 잘 모르는 사람이 질문하는 것을
부끄럽게 느끼지 않도록 편안하게 설명해주세요.

"야구를 같이 보면서 알려주는 친구"처럼
설명해주세요.
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
# 11. CONVERSATION
# ============================================================

if st.session_state.messages:

    st.markdown(
        dedent(
            """
            <div class="chat-section">

                <div class="section-header">
                    <div>
                        <div class="section-label">
                            CONVERSATION
                        </div>

                        <div class="section-title">
                            야구를 함께 알아볼게요.
                        </div>
                    </div>
                </div>

            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# ============================================================
# 12. STARTER QUESTIONS
# ============================================================

if not st.session_state.messages:

    st.markdown(
        dedent(
            """
            <div class="section-header">
                <div>
                    <div class="section-label">
                        START WITH A QUESTION
                    </div>

                    <div class="section-title">
                        궁금한 것부터 시작하세요.
                    </div>
                </div>

                <div class="section-count">
                    BEGINNER
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "스트라이크와 볼은 뭐가 달라?",
            key="starter_rule",
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

            st.session_state.pending_question = True
            st.rerun()

    with col2:

        if st.button(
            "병살은 어떻게 만들어져?",
            key="starter_double_play",
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

            st.session_state.pending_question = True
            st.rerun()

    col3, col4 = st.columns(2)

    with col3:

        if st.button(
            "OPS가 높으면 좋은 선수야?",
            key="starter_ops",
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

            st.session_state.pending_question = True
            st.rerun()

    with col4:

        if st.button(
            "포스 아웃과 태그 아웃의 차이는?",
            key="starter_out",
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

            st.session_state.pending_question = True
            st.rerun()


# ============================================================
# 13. STARTER QUESTION RESPONSE
# ============================================================

if (
    st.session_state.pending_question
    and st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
):

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

    st.session_state.pending_question = None


# ============================================================
# 14. FREE QUESTION
# ============================================================

if prompt := st.chat_input(
    "야구에 대해 궁금한 것을 물어보세요..."
):

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
    dedent(
        """
        <div class="footer">
            <div>KBO BASEBALL LEARNING</div>
            <div>RULE · TERM · STATS · SITUATION</div>
        </div>
        """
    ),
    unsafe_allow_html=True,
)
