import streamlit as st
from openai import OpenAI


# ============================================================
# 1. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="KBO Baseball Learning",
    page_icon="⚾",
    layout="wide",
)


# ============================================================
# 2. COLORS
# ============================================================

ORANGE = "#FF5722"
BLACK = "#111111"
WHITE = "#FFFFFF"
BG = "#F5F5F3"
GRAY_100 = "#EEEEEC"
GRAY_200 = "#DDDDD9"
GRAY_500 = "#888888"
GRAY_700 = "#444444"


# ============================================================
# 3. CSS
#    HTML CONTENT를 만들지 않고 CSS만 사용합니다.
# ============================================================

st.markdown(
    f"""
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {{
        background-color: {BG};
        color: {BLACK};
    }}

    .block-container {{
        max-width: 1160px;
        padding-top: 42px;
        padding-bottom: 80px;
    }}

    header {{
        visibility: hidden;
    }}

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    * {{
        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Pretendard",
            "Noto Sans KR",
            "Apple SD Gothic Neo",
            "Segoe UI",
            sans-serif;
    }}


    /* ========================================================
       TOP BRAND
       ======================================================== */

    .brand-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }}

    .brand {{
        font-size: 15px;
        font-weight: 900;
        letter-spacing: 0.08em;
        color: {BLACK};
    }}

    .brand-dot {{
        display: inline-block;
        width: 9px;
        height: 9px;
        margin-right: 8px;
        border-radius: 50%;
        background-color: {ORANGE};
    }}

    .brand-meta {{
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.12em;
        color: #999999;
    }}


    /* ========================================================
       HERO
       ======================================================== */

    .hero-box {{
        position: relative;
        overflow: hidden;
        min-height: 350px;
        padding: 48px 52px;
        margin-bottom: 46px;
        border-radius: 24px;
        background-color: {BLACK};
        box-sizing: border-box;
    }}

    .hero-kicker {{
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.16em;
        color: {ORANGE};
        margin-bottom: 23px;
    }}

    .hero-title {{
        margin: 0;
        color: {WHITE};
        font-size: clamp(46px, 6vw, 76px);
        line-height: 0.98;
        font-weight: 950;
        letter-spacing: -0.065em;
    }}

    .hero-title-orange {{
        color: {ORANGE};
    }}

    .hero-description {{
        margin-top: 26px;
        max-width: 500px;
        color: #A7A7A7;
        font-size: 14px;
        line-height: 1.75;
    }}

    .hero-year {{
        position: absolute;
        right: 46px;
        bottom: 27px;
        color: rgba(255,255,255,0.08);
        font-size: 120px;
        font-weight: 950;
        line-height: 0.8;
        letter-spacing: -0.08em;
    }}


    /* ========================================================
       BASEBALL GRAPHIC
       ======================================================== */

    .baseball {{
        position: absolute;
        right: 105px;
        top: 78px;
        width: 155px;
        height: 155px;
        border-radius: 50%;
        background: {WHITE};
        transform: rotate(-20deg);
        box-shadow: 0 25px 60px rgba(0,0,0,0.30);
    }}

    .baseball-stitch-left {{
        position: absolute;
        left: 42px;
        top: -5px;
        width: 48px;
        height: 165px;
        border-right: 3px dashed {ORANGE};
        border-radius: 50%;
        transform: rotate(12deg);
    }}

    .baseball-stitch-right {{
        position: absolute;
        right: 42px;
        top: -5px;
        width: 48px;
        height: 165px;
        border-left: 3px dashed {ORANGE};
        border-radius: 50%;
        transform: rotate(12deg);
    }}


    /* ========================================================
       SECTION
       ======================================================== */

    .section-top {{
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 17px;
    }}

    .section-label {{
        margin-bottom: 6px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.15em;
        color: {ORANGE};
    }}

    .section-title {{
        font-size: 25px;
        font-weight: 900;
        letter-spacing: -0.05em;
        color: {BLACK};
    }}

    .section-count {{
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.1em;
        color: #999999;
    }}


    /* ========================================================
       CATEGORY BUTTONS
       ======================================================== */

    div.stButton > button {{
        width: 100%;
        min-height: 185px;
        padding: 25px;
        border: 1px solid {GRAY_200};
        border-radius: 18px;
        background: {WHITE};
        color: {BLACK};
        text-align: left;
        white-space: pre-wrap;
        box-shadow: none;
        transition:
            transform 0.15s ease,
            border-color 0.15s ease,
            box-shadow 0.15s ease;
    }}

    div.stButton > button:hover {{
        border-color: {BLACK};
        background: {WHITE};
        color: {BLACK};
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.07);
    }}

    div.stButton > button:active {{
        transform: translateY(-1px);
    }}

    div.stButton > button p {{
        font-size: 14px;
        line-height: 1.7;
    }}


    /* ========================================================
       QUESTION BUTTONS
       ======================================================== */

    .question-area {{
        margin-top: 34px;
        padding: 28px;
        border-radius: 20px;
        background: {BLACK};
    }}

    .question-label {{
        margin-bottom: 7px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.15em;
        color: {ORANGE};
    }}

    .question-heading {{
        margin-bottom: 20px;
        color: {WHITE};
        font-size: 22px;
        font-weight: 900;
        letter-spacing: -0.04em;
    }}

    .question-area div.stButton > button {{
        min-height: 58px;
        padding: 15px 18px;
        border: 1px solid #303030;
        border-radius: 11px;
        background: #1B1B1B;
        color: #EAEAEA;
    }}

    .question-area div.stButton > button:hover {{
        border-color: {ORANGE};
        background: #1B1B1B;
        color: {WHITE};
        transform: none;
    }}


    /* ========================================================
       API AREA
       ======================================================== */

    .api-heading {{
        margin-top: 38px;
        margin-bottom: 8px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.15em;
        color: #888888;
    }}

    .api-description {{
        margin-bottom: 8px;
        font-size: 12px;
        color: #999999;
    }}

    div[data-testid="stTextInput"] input {{
        border: 1px solid {GRAY_200};
        border-radius: 10px;
        background: {WHITE};
    }}

    div[data-testid="stTextInput"] input:focus {{
        border-color: {ORANGE};
        box-shadow: 0 0 0 1px {ORANGE};
    }}


    /* ========================================================
       CHAT
       ======================================================== */

    .chat-header {{
        margin-top: 38px;
        margin-bottom: 18px;
        padding-top: 28px;
        border-top: 1px solid {GRAY_200};
    }}

    .chat-label {{
        margin-bottom: 5px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.15em;
        color: {ORANGE};
    }}

    .chat-title {{
        font-size: 25px;
        font-weight: 900;
        letter-spacing: -0.05em;
        color: {BLACK};
    }}

    [data-testid="stChatMessage"] {{
        padding-top: 10px;
        padding-bottom: 10px;
        background: transparent;
    }}

    [data-testid="stChatMessageContent"] {{
        font-size: 15px;
        line-height: 1.8;
    }}

    [data-testid="stChatInput"] textarea {{
        border: 1px solid {GRAY_200};
        border-radius: 13px;
        background: {WHITE};
    }}

    [data-testid="stChatInput"] textarea:focus {{
        border-color: {ORANGE};
        box-shadow: 0 0 0 1px {ORANGE};
    }}


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-line {{
        height: 1px;
        margin-top: 60px;
        margin-bottom: 16px;
        background: {GRAY_200};
    }}

    .footer-text {{
        display: flex;
        justify-content: space-between;
        color: #999999;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 0.1em;
    }}


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {{

        .block-container {{
            padding: 25px 18px 60px 18px;
        }}

        .brand-meta {{
            display: none;
        }}

        .hero-box {{
            min-height: 400px;
            padding: 35px 28px;
            border-radius: 18px;
        }}

        .hero-title {{
            font-size: 48px;
        }}

        .hero-description {{
            max-width: 290px;
        }}

        .baseball {{
            right: 35px;
            top: auto;
            bottom: 40px;
            width: 100px;
            height: 100px;
        }}

        .baseball-stitch-left,
        .baseball-stitch-right {{
            height: 108px;
            width: 32px;
            border-width: 2px;
        }}

        .baseball-stitch-left {{
            left: 27px;
        }}

        .baseball-stitch-right {{
            right: 27px;
        }}

        .hero-year {{
            display: none;
        }}

        .section-title {{
            font-size: 21px;
        }}

        div.stButton > button {{
            min-height: 155px;
        }}

        .question-area {{
            padding: 22px 18px;
        }}

        .footer-text {{
            flex-direction: column;
            gap: 8px;
        }}
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ============================================================
# 5. TOP BRAND
# ============================================================

brand_col1, brand_col2 = st.columns([3, 1])

with brand_col1:
    st.markdown(
        '<div class="brand"><span class="brand-dot"></span>KBO BASEBALL</div>',
        unsafe_allow_html=True,
    )

with brand_col2:
    st.markdown(
        '<div class="brand-meta">AI BASEBALL LEARNING</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# 6. HERO
# ============================================================

hero_left, hero_right = st.columns([2.2, 1])

with hero_left:

    st.markdown(
        '<div class="hero-box">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="hero-kicker">KBO BASEBALL LEARNING</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-title">
            야구를 보다,<br>
            <span class="hero-title-orange">이해하다.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-description">
            야구가 처음이어도 괜찮아요.<br>
            KBO의 규칙, 용어, 기록과 경기 상황을<br>
            AI와 함께 하나씩 배워보세요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="hero-year">26</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="baseball"><div class="baseball-stitch-left"></div><div class="baseball-stitch-right"></div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# 7. API KEY
# ============================================================

st.markdown(
    '<div class="api-heading">OPENAI API KEY</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="api-description">챗봇을 사용하려면 OpenAI API Key가 필요합니다.</div>',
    unsafe_allow_html=True,
)

openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-...",
    label_visibility="collapsed",
)


# ============================================================
# 8. API KEY가 없을 때
# ============================================================

if not openai_api_key:

    st.markdown(
        """
        <div class="section-top">
            <div>
                <div class="section-label">LEARN BASEBALL</div>
                <div class="section-title">무엇부터 알아볼까요?</div>
            </div>

            <div class="section-count">04 CATEGORIES</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "01 / RULE\n\n야구 규칙\n\n스트라이크, 볼, 아웃부터 포스 아웃과 태그 아웃까지",
            key="category_rule",
        ):
            st.session_state.pending_question = (
                "야구의 기본 규칙을 초보자에게 쉽게 설명해줘. "
                "특히 스트라이크, 볼, 아웃, 이닝이 무엇인지 알려줘."
            )
            st.rerun()

    with col2:

        if st.button(
            "02 / TERM\n\n야구 용어\n\n병살, 희생플라이, 도루 등 경기에서 자주 듣는 용어",
            key="category_term",
        ):
            st.session_state.pending_question = (
                "야구 초보자가 알아두면 좋은 대표적인 야구 용어를 "
                "10개 정도 골라서 쉽게 설명해줘."
            )
            st.rerun()

    col3, col4 = st.columns(2)

    with col3:

        if st.button(
            "03 / STATS\n\n야구 기록\n\n타율, 출루율, 장타율, OPS, ERA, WHIP 이해하기",
            key="category_stats",
        ):
            st.session_state.pending_question = (
                "야구 기록 중 타율, 출루율, 장타율, OPS, ERA, WHIP을 "
                "야구 초보자에게 쉽게 설명하고 서로 비교해줘."
            )
            st.rerun()

    with col4:

        if st.button(
            "04 / SITUATION\n\n경기 상황\n\n실제 경기 장면을 통해 플레이의 결과 이해하기",
            key="category_situation",
        ):
            st.session_state.pending_question = (
                "야구 경기 상황을 하나 예시로 만들어서 "
                "주자 위치, 아웃 카운트, 타구, 수비 행동, 결과까지 "
                "초보자가 이해할 수 있도록 분석해줘."
            )
            st.rerun()

    # --------------------------------------------------------
    # Popular Questions
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="question-area">

            <div class="question-label">
                POPULAR QUESTIONS
            </div>

            <div class="question-heading">
                이런 것부터 물어보세요.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    q1, q2 = st.columns(2)

    with q1:

        if st.button(
            "스트라이크와 볼은 뭐가 달라?",
            key="question_1",
        ):
            st.session_state.pending_question = (
                "스트라이크와 볼은 무엇이 다른지 "
                "야구를 처음 보는 사람도 이해할 수 있게 설명해줘."
            )
            st.rerun()

        if st.button(
            "병살은 어떻게 만들어져?",
            key="question_2",
        ):
            st.session_state.pending_question = (
                "야구에서 병살이 무엇인지 설명해줘. "
                "1루에 주자가 있고 타자가 땅볼을 쳤을 때를 예로 들어줘."
            )
            st.rerun()

    with q2:

        if st.button(
            "OPS가 높으면 좋은 선수야?",
            key="question_3",
        ):
            st.session_state.pending_question = (
                "OPS가 무엇인지 설명해줘. "
                "OPS가 높다는 것이 타자에게 어떤 의미인지 "
                "실제 야구를 볼 때 이해할 수 있도록 설명해줘."
            )
            st.rerun()

        if st.button(
            "포스 아웃과 태그 아웃의 차이는?",
            key="question_4",
        ):
            st.session_state.pending_question = (
                "포스 아웃과 태그 아웃의 차이를 "
                "실제 경기 상황을 예로 들어서 쉽게 설명해줘."
            )
            st.rerun()


# ============================================================
# 9. OPENAI CLIENT
# ============================================================

if openai_api_key:

    client = OpenAI(
        api_key=openai_api_key
    )


    # ========================================================
    # 10. SYSTEM PROMPT
    # ========================================================

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
    ④ 왜 중요한지 설명
    ⑤ 비슷한 개념과 비교

    단순한 사전식 정의로 끝내지 말고
    사용자가 실제 KBO 경기를 볼 때
    이해할 수 있도록 설명해주세요.


    [초보자 배려]

    야구를 처음 보는 사람도 이해할 수 있도록
    전문 용어를 연속해서 사용하지 마세요.

    사용자가 잘못 이해하고 있다면
    부드럽게 교정해주세요.

    설명이 복잡한 경우에는 표나 bullet point를
    적극적으로 사용하세요.


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
    →
    주자 위치
    →
    아웃 카운트
    →
    타구
    →
    수비 행동
    →
    주자 행동
    →
    결과

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
    최신 데이터가 제공되지 않았다면 추측하지 마세요.

    확실하지 않은 정보는
    확실하지 않다고 알려주세요.


    [말투]

    친절하고 차분하게 설명해주세요.

    야구를 잘 모르는 사람이 질문하는 것을
    부끄럽게 느끼지 않도록 편안하게 설명해주세요.

    '야구를 같이 보면서 알려주는 친구'처럼
    설명해주세요.
    """


    # ========================================================
    # 11. RESPONSE FUNCTION
    # ========================================================

    def get_response():

        return client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                }
            ]
            + st.session_state.messages,
            stream=True,
        )


    # ========================================================
    # 12. PENDING QUESTION
    # ========================================================

    if st.session_state.pending_question:

        question = st.session_state.pending_question

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        st.session_state.pending_question = None

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


    # ========================================================
    # 13. EXISTING CHAT
    # ========================================================

    if st.session_state.messages:

        st.markdown(
            """
            <div class="chat-header">
                <div class="chat-label">CONVERSATION</div>
                <div class="chat-title">야구를 함께 알아볼게요.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])


    # ========================================================
    # 14. CHAT INPUT
    # ========================================================

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
            })


# ============================================================
# 15. FOOTER
# ============================================================

st.markdown(
    '<div class="footer-line"></div>',
    unsafe_allow_html=True,
)

footer_left, footer_right = st.columns([2, 1])

with footer_left:
    st.markdown(
        '<div class="footer-text">KBO BASEBALL LEARNING</div>',
        unsafe_allow_html=True,
    )

with footer_right:
    st.markdown(
        '<div class="footer-text">RULE · TERM · STATS · SITUATION</div>',
        unsafe_allow_html=True,
    )
