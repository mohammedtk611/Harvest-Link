import streamlit as st

# ==================================================
# THEME DEFINITIONS
# ==================================================

THEMES = {
    "Dark": {
        "bg": "#0e1117",
        "text": "#e5e7eb",
        "card": "#161b22",
        "accent": "#22c55e",
        "border": "#30363d",
        "sidebar_bg": "#0e1117",
        "sidebar_text": "#e5e7eb",
        "sidebar_hover": "#1f2937"
    },
    "Light": {
        "bg": "#f9fafb",
        "text": "#111827",
        "card": "#ffffff",
        "accent": "#2563eb",
        "border": "#BEC8DC",
        "sidebar_bg": "#1e293b",
        "sidebar_text": "#ffffff",
        "sidebar_hover": "#334155"
    },
    "Earth": {
        "bg": "#f3efe0",
        "text": "#2c140f",
        "card": "#fff8e1",
        "accent": "#8d6e63",
        "border": "#d7ccc8",
        "sidebar_bg": "#4e342e",
        "sidebar_text": "#efebe9",
        "sidebar_hover": "#5d4037"
    },
    "Eco": {
        "bg": "#e8f5e9",
        "text": "#1b5e20",
        "card": "#ffffff",
        "accent": "#2e7d32",
        "border": "#c8e6c9",
        "sidebar_bg": "#1b5e20",
        "sidebar_text": "#ffffff",
        "sidebar_hover": "#2e7d32"
    }
}

# ==================================================
# APPLY THEME (WITH RESET – FIXES TOGGLE BUG)
# ==================================================

def apply_theme(theme_name: str = "Dark"):
    # Reset previous CSS (IMPORTANT)
    st.markdown("<style id='theme-reset'></style>", unsafe_allow_html=True)

    t = THEMES.get(theme_name, THEMES["Dark"])

    st.markdown(
        f"""
        <style>

        /* App background */
        .stApp {{
            background-color: {t['bg']};
            color: {t['text']};
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(
                180deg,
                {t['accent']},
                {t['sidebar_bg']}
            );
            border-right: 1px solid {t['border']};
        }}

        /* Sidebar text */
        section[data-testid="stSidebar"] * {{
            color: {t['sidebar_text']} !important;
            font-weight: 500;
        }}

        /* Navigation radio items */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label {{
            padding: 10px 14px;
            border-radius: 10px;
            margin-bottom: 6px;
            transition: all 0.2s ease-in-out;
        }}

        /* Hover */
        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
            background-color: {t['sidebar_hover']};
        }}

        /* Selected */
        section[data-testid="stSidebar"]
        div[role="radiogroup"] input:checked + div {{
            background-color: rgba(255, 255, 255, 0.18);
            border-radius: 10px;
        }}

        /* Headings */
        h1, h2, h3, h4 {{
            color: {t['text']};
        }}

        /* Metric cards */
        div[data-testid="stMetric"] {{
            background-color: {t['card']};
            border-left: 6px solid {t['accent']};
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        }}

        /* Custom cards */
        .card {{
            background-color: {t['card']};
            border-radius: 16px;
            padding: 20px;
            border: 1px solid {t['border']};
            box-shadow: 0 6px 18px rgba(0,0,0,0.08);
            margin-bottom: 16px;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: {t['accent']};
            color: white;
            border-radius: 10px;
            padding: 10px 18px;
            border: none;
            font-weight: 600;
        }}

        .stButton > button:hover {{
            opacity: 0.9;
            transform: scale(1.02);
        }}

        /* Dataframes */
        .stDataFrame {{
            border-radius: 14px;
            border: 1px solid {t['border']};
        }}

        </style>
        """,
        unsafe_allow_html=True
    )
