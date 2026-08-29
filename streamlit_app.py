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
           CLICKABLE CATEGORY CARDS

           st.container(key="...") makes Streamlit add a
           ".st-key-<key>" class to that container's wrapper
           div. The outer "card-*" container just needs to be
           a positioning + hover context. The INNER
           "card-overlay-*" container is the one that actually
           gets turned into an invisible button on top of the
           card -- kept separate from the outer container so
           that the "more info" button that appears after a
           card is expanded (a normal, visible button) is NOT
           accidentally made invisible too.
        ==================================================== */

        [class*="st-key-card-"] {
            position: relative;
            cursor: pointer;
        }

        [class*="st-key-card-"]:hover .category-card {
            border-color: #111111;
            transform: translateY(-2px);
        }

        [class*="st-key-card-overlay-"] {
            position: absolute;
            inset: 0;
            margin: 0;
            z-index: 5;
        }

        [class*="st-key-card-overlay-"] [data-testid="stButton"] button {
            width: 100%;
            height: 100%;
            border-radius: 18px;
            border: none;
            background: transparent;
            color: transparent;
            box-shadow: none;
            cursor: pointer;
        }


        /* ====================================================
           CATEGORY SUMMARY PREVIEW
           (shown instantly when a card is clicked, no API
           call needed)
        ==================================================== */

        @keyframes summaryFadeIn {
            from {
                opacity: 0;
                transform: translateY(-6px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .category-summary {
            background: #FFFFFF;
            border: 1px solid #E1E1DE;
            border-left: 4px solid #FF5722;
            border-radius: 4px 16px 16px 4px;
            padding: 18px 20px;
            margin-top: -6px;
            margin-bottom: 14px;
            animation: summaryFadeIn 0.2s ease;
        }

        .category-summary-label {
            font-size: 10px;
            font-weight: 900;
            letter-spacing: 0.12em;
            color: #FF5722;
            margin-bottom: 8px;
        }

        .category-summary-text {
            font-size: 13px;
            line-height: 1.75;
            color: #333333;
        }


        /* ====================================================
           TEAM PICKER
        ==================================================== */

        .team-section {
            background: #FFFFFF;
            border: 1px solid #E1E1DE;
            border-radius: 16px;
            padding: 20px 22px;
            margin-bottom: 24px;
        }

        .team-label {
            font-size: 10px;
            font-weight: 900;
            letter-spacing: 0.13em;
            color: #888888;
            margin-bottom: 8px;
        }

        .team-description {
            font-size: 12px;
            color: #999999;
            margin-bottom: 14px;
        }

        .team-selected-tag {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            border-radius: 999px;
            padding: 5px 14px;
            font-size: 11px;
            font-weight: 800;
            margin-bottom: 14px;
        }

        [class*="st-key-team-"] button {
            border-radius: 999px !important;
            padding: 8px 6px !important;
            font-size: 12px !important;
        }


        /* ====================================================
           GENERAL STREAMLIT BUTTONS (starter questions, etc.)
        ==================================================== */

        .stButton > button {
            width: 100%;
            border-radius: 14px;
            border: 1px solid #E1E1DE;
            background: #FFFFFF;
            color: #111111;
            font-weight: 700;
            font-size: 14px;
            padding: 14px 18px;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            border-color: #FF5722;
            color: #FF5722;
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
            background: #FFFFFF;
            border: 1px solid #E1E1DE;
            border-radius: 16px;
            padding: 16px 18px;
            margin-bottom: 14px;
            box-shadow: 0 2px 8px rgba(17, 17, 17, 0.03);
        }

        [data-testid="stChatMessageContent"] {
            font-size: 15px;
            line-height: 1.8;
        }

        /* The chat input lives in a bar pinned to the bottom of
           the viewport. By default it's easy to miss against a
           page that already has a lot going on, so we give the
           whole bar a clear surface, a top border/shadow to
           separate it from scrolling content, and align its
           width with the rest of the page. Selectors are
           listed for a couple of possible Streamlit test-ids
           since the internal name has changed across versions
           -- unmatched ones are simply ignored. */

        [data-testid="stBottom"] {
            background: #F4F4F2;
            border-top: 1px solid #E1E1DE;
            box-shadow: 0 -6px 20px rgba(17, 17, 17, 0.05);
        }

        [data-testid="stBottomBlockContainer"] {
            max-width: 1180px;
            padding-top: 16px;
            padding-bottom: 20px;
        }

        [data-testid="stChatInput"] {
            padding-top: 0;
        }

        [data-testid="stChatInput"] textarea {
            border: 1px solid #D8D8D5;
            border-radius: 16px;
            background: #FFFFFF;
            font-size: 14px;
            padding: 14px 16px;
        }

        [data-testid="stChatInput"] textarea:focus {
            border-color: #FF5722;
            box-shadow: 0 0 0 2px rgba(255, 87, 34, 0.18);
        }

        [data-testid="stChatInput"] button {
            background: #FF5722 !important;
            border-radius: 50% !important;
            border: none !important;
        }

        [data-testid="stChatInput"] button svg {
            fill: #FFFFFF !important;
        }

        /* Leave enough room at the bottom of the scrollable
           content so the last chat message isn't hidden behind
           the fixed input bar above. */
        .block-container {
            padding-bottom: 140px;
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

if "expanded_category" not in st.session_state:
    st.session_state.expanded_category = None

if "favorite_team" not in st.session_state:
    st.session_state.favorite_team = None


# ============================================================
# 4. CATEGORY DATA
# (used to render the 4 category cards: "summary" is shown
#  instantly with no API call, "question" is only sent to the
#  chatbot if the user asks for more)
# ============================================================

CATEGORIES = [
    {
        "key": "rule",
        "number": "01 / RULE",
        "title": "야구 규칙",
        "description": "스트라이크와 볼부터 아웃, 이닝, 포스 아웃과 태그 아웃까지",
        "summary": (
            "스트라이크는 타자가 쳐야 할 좋은 공, 볼은 벗어난 공이에요. "
            "스트라이크 3개면 삼진 아웃, 볼 4개면 타자가 1루로 걸어나가는 "
            "볼넷이 됩니다. 아웃을 3번 잡으면 그 팀의 공격(이닝)이 끝나요."
        ),
        "question": (
            "야구의 기본 규칙인 스트라이크, 볼, 아웃, 이닝, "
            "포스 아웃과 태그 아웃의 차이를 야구 초보자에게 쉽게 설명해줘."
        ),
    },
    {
        "key": "term",
        "number": "02 / TERM",
        "title": "야구 용어",
        "description": "병살, 희생플라이, 도루, 야수선택 등 경기에서 자주 듣는 용어",
        "summary": (
            "병살은 타자와 주자 두 명을 한 번에 아웃시키는 것, 도루는 주자가 "
            "다음 베이스로 몰래 뛰어가는 것을 말해요. 중계에서 자주 나오는 "
            "이런 용어들을 알면 경기 흐름이 훨씬 잘 읽힙니다."
        ),
        "question": (
            "병살, 희생플라이, 도루, 야수선택처럼 경기에서 자주 나오는 "
            "야구 용어들을 하나씩 쉽게 설명해줘."
        ),
    },
    {
        "key": "stats",
        "number": "03 / STATS",
        "title": "야구 기록",
        "description": "타율, 출루율, 장타율, OPS, ERA, WHIP 등을 쉽게 이해하기",
        "summary": (
            "타율은 타석에서 안타를 칠 확률, OPS는 출루율과 장타율을 더한 "
            "값으로 타자의 전체적인 공격력을 보여줘요. ERA는 투수가 9이닝 "
            "동안 내주는 평균 실점으로, 낮을수록 좋은 투수라는 뜻입니다."
        ),
        "question": (
            "타율, 출루율, 장타율, OPS, ERA, WHIP이 각각 무엇을 의미하는지 "
            "야구 초보자에게 쉽게 설명해줘."
        ),
    },
    {
        "key": "situation",
        "number": "04 / SITUATION",
        "title": "경기 상황",
        "description": "실제 경기에서 왜 이런 결과가 나왔는지 상황별로 하나씩 분석하기",
        "summary": (
            "주자 위치, 아웃 카운트, 타구 방향에 따라 수비 팀의 선택이 "
            "달라져요. 예를 들어 1루에 주자가 있고 무사 상황이면 병살을 "
            "노리는 수비가 자주 나옵니다. 상황을 하나씩 뜯어보면 왜 그런 "
            "결과가 나왔는지 보이기 시작해요."
        ),
        "question": (
            "실제 경기에서 자주 나오는 상황을 하나 예로 들어서, 주자 위치와 "
            "아웃 카운트에 따라 왜 그런 수비 결과가 나왔는지 분석하는 방법을 알려줘."
        ),
    },
]


def render_category_card(category):
    """Render one category card.

    The card itself has a real (visually hidden) button overlaid
    on top of it, scoped via a nested st.container(key=...) so it
    doesn't affect any other button in the app. Clicking it just
    toggles a free, instant text summary open/closed -- no API
    call. Only the extra "챗봇에게 더 물어보기" button inside the
    summary actually sends a question to the chatbot.
    """

    key = category["key"]

    with st.container(key=f"card-{key}"):

        st.html(
            dedent(
                f"""
                <div class="category-card">
                    <div class="category-number">{category['number']}</div>
                    <div class="category-title">{category['title']}</div>
                    <div class="category-description">
                        {category['description']}
                    </div>
                    <div class="category-arrow">↗</div>
                </div>
                """
            )
        )

        with st.container(key=f"card-overlay-{key}"):
            toggled = st.button(category["title"], key=f"card-btn-{key}")

        if toggled:
            if st.session_state.expanded_category == key:
                st.session_state.expanded_category = None
            else:
                st.session_state.expanded_category = key

        if st.session_state.expanded_category == key:

            st.html(
                dedent(
                    f"""
                    <div class="category-summary">
                        <div class="category-summary-label">{category['number']}</div>
                        <div class="category-summary-text">{category['summary']}</div>
                    </div>
                    """
                )
            )

            if st.button(
                "챗봇에게 더 물어보기",
                key=f"card-ask-{key}",
                use_container_width=True,
            ):
                # Overwrite (not append) so only the most recently
                # asked category is queued up.
                st.session_state.messages = [
                    {"role": "user", "content": category["question"]}
                ]
                st.session_state.pending_question = True
                st.rerun()


# ============================================================
# 4B. TEAM DATA
# (used for the optional "응원팀" picker; the selected team
#  both personalizes the chatbot's answers and re-colors the
#  page's accent color)
# ============================================================

TEAMS = [
    {"key": "doosan", "name": "두산 베어스", "color": "#131230"},
    {"key": "lg", "name": "LG 트윈스", "color": "#C30452"},
    {"key": "kt", "name": "KT 위즈", "color": "#EB1C24"},
    {"key": "ssg", "name": "SSG 랜더스", "color": "#CE0E2D"},
    {"key": "nc", "name": "NC 다이노스", "color": "#315288"},
    {"key": "lotte", "name": "롯데 자이언츠", "color": "#041E42"},
    {"key": "samsung", "name": "삼성 라이온즈", "color": "#074CA1"},
    {"key": "hanwha", "name": "한화 이글스", "color": "#FF6600"},
    {"key": "kia", "name": "KIA 타이거즈", "color": "#EA0029"},
    {"key": "kiwoom", "name": "키움 히어로즈", "color": "#570514"},
]

TEAMS_BY_KEY = {t["key"]: t for t in TEAMS}


def render_team_picker():
    """Optional team picker. Selecting a team both nudges the
    chatbot to use that team's examples, and re-colors the
    page's orange accent to match the team."""

    st.html(
        dedent(
            """
            <div class="team-section">
                <div class="team-label">MY TEAM (선택)</div>
                <div class="team-description">
                    응원하는 팀을 고르면 그 팀 이야기를 곁들여서 설명해 드려요.
                </div>
            </div>
            """
        )
    )

    selected = st.session_state.favorite_team

    if selected:
        team = TEAMS_BY_KEY[selected]
        st.html(
            dedent(
                f"""
                <div class="team-selected-tag"
                     style="background:{team['color']}22;color:{team['color']};">
                    ⚾ {team['name']} 팬으로 설정됨
                </div>
                """
            )
        )

    cols = st.columns(5)

    for i, team in enumerate(TEAMS):
        with cols[i % 5]:
            with st.container(key=f"team-{team['key']}"):
                if st.button(team["name"], key=f"team-btn-{team['key']}"):
                    if st.session_state.favorite_team == team["key"]:
                        st.session_state.favorite_team = None
                    else:
                        st.session_state.favorite_team = team["key"]
                    st.rerun()

    # Give every team chip its own outline color, and fill in
    # the currently-selected one solid.
    chip_rules = []

    for team in TEAMS:
        chip_rules.append(
            f'[class*="st-key-team-{team["key"]}"] button '
            f'{{ border-color: {team["color"]}; color: {team["color"]}; }}'
        )

    if selected:
        team = TEAMS_BY_KEY[selected]
        chip_rules.append(
            f'[class*="st-key-team-{team["key"]}"] button {{ '
            f'background: {team["color"]} !important; '
            f'color: #FFFFFF !important; }}'
        )

    st.markdown(
        f"<style>{' '.join(chip_rules)}</style>",
        unsafe_allow_html=True,
    )

    # If a team is selected, retheme the site's orange accent
    # color to that team's color.
    if selected:
        team = TEAMS_BY_KEY[selected]
        st.markdown(
            dedent(
                f"""
                <style>
                .hero-kicker {{
                    background: {team['color']} !important;
                }}
                .hero-title .orange {{
                    color: {team['color']} !important;
                }}
                .category-number {{
                    color: {team['color']} !important;
                }}
                .category-summary {{
                    border-left-color: {team['color']} !important;
                }}
                .category-summary-label {{
                    color: {team['color']} !important;
                }}
                .questions-wrapper .section-label {{
                    color: {team['color']} !important;
                }}
                .question-arrow {{
                    color: {team['color']} !important;
                }}
                .stButton > button:hover {{
                    border-color: {team['color']} !important;
                    color: {team['color']} !important;
                }}
                </style>
                """
            ),
            unsafe_allow_html=True,
        )


# ============================================================
# 5. TOP BRAND
# ============================================================

st.html(
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
    )
)


# ============================================================
# 6. HERO
# ============================================================

st.html(
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
    )
)


# ============================================================
# 7. API KEY AREA
# ============================================================

st.html(
    dedent(
        """
        <div class="api-section">
            <div class="api-label">OPENAI API KEY</div>
            <div class="api-description">
                API Key를 입력하면 야구 학습 챗봇을 사용할 수 있습니다.
            </div>
        </div>
        """
    )
)

openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-...",
    label_visibility="collapsed",
)

if st.session_state.pending_question and not openai_api_key:
    st.info("질문이 준비됐어요! 위에 API Key를 입력하면 바로 답변해 드릴게요.")


# ============================================================
# 8. TEAM PICKER + CATEGORY CARDS
# (always visible, regardless of whether an API key has been
#  entered yet -- only the actual chat below requires a key)
# ============================================================

render_team_picker()

st.html(
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
    )
)

col1, col2 = st.columns(2)

with col1:
    render_category_card(CATEGORIES[0])

with col2:
    render_category_card(CATEGORIES[1])

col3, col4 = st.columns(2)

with col3:
    render_category_card(CATEGORIES[2])

with col4:
    render_category_card(CATEGORIES[3])

if not st.session_state.messages:

    st.html(
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
        )
    )


if openai_api_key:

    # ============================================================
    # 9. OPENAI CLIENT
    # ============================================================

    client = OpenAI(
        api_key=openai_api_key
    )


    # ============================================================
    # 10. SYSTEM PROMPT
    # ============================================================

    system_prompt = dedent(
        """
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
    )

    if st.session_state.favorite_team:
        _team_name = TEAMS_BY_KEY[st.session_state.favorite_team]["name"]
        system_prompt += dedent(
            f"""

            [사용자 응원팀]

            사용자는 {_team_name}을(를) 응원하는 팬입니다.
            가능하면 설명할 때 이 팀과 관련된 예시를 자연스럽게
            곁들여 주세요.

            다만 최신 선수 명단, 최근 경기 결과, 순위처럼
            실시간 정보가 필요한 내용은 확실하지 않다면
            추측하지 말고 모른다고 알려주세요.
            """
        )


    # ============================================================
    # 11. RESPONSE FUNCTION
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
    # 12. CONVERSATION
    # ============================================================

    if st.session_state.messages:

        st.html(
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
            )
        )

        for message in st.session_state.messages:

            avatar = "⚾" if message["role"] == "assistant" else "🧑"

            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])


    # ============================================================
    # 13. STARTER QUESTIONS
    # ============================================================

    if not st.session_state.messages:

        st.html(
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
            )
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
    # 14. STARTER QUESTION RESPONSE
    # ============================================================

    if (
        st.session_state.pending_question
        and st.session_state.messages
        and st.session_state.messages[-1]["role"] == "user"
    ):

        with st.chat_message("assistant", avatar="⚾"):

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
    # 15. FREE QUESTION
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

        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="⚾"):

            response = st.write_stream(
                get_response()
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )



else:

    st.info("위에 OpenAI API Key를 입력하면 여기서 바로 채팅으로 물어볼 수 있어요.")


# ============================================================
# 16. FOOTER
# ============================================================

st.html(
    dedent(
        """
        <div class="footer">
            <div>KBO BASEBALL LEARNING</div>
            <div>RULE · TERM · STATS · SITUATION</div>
        </div>
        """
    )
)
