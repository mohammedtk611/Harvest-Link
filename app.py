import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components

# ---------------- IMPORT VIEWS ----------------
from views import dashboard, storage, market, services, profile, impact
from utils.style import apply_theme

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="HarvestLink",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- THEME STATE (CRITICAL FIX) ----------------
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

selected_theme = st.sidebar.selectbox(
    "🎨 Choose Theme",
    ["Light", "Dark", "Earth", "Eco"],
    index=["Light", "Dark", "Earth", "Eco"].index(st.session_state.theme)
)

# Force rerun on theme change
if selected_theme != st.session_state.theme:
    st.session_state.theme = selected_theme
    st.rerun()

# Apply theme AFTER state settles
apply_theme(st.session_state.theme)

# ---------------- SIDEBAR LOGO ----------------
LOGO_PATH = Path("assests/harvestlink_logo.jpeg")

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)

        st.markdown(
            """
            <p style="
                text-align:center;
                font-size:13px;
                margin-top:-8px;
                opacity:0.9;
            ">
            Connecting Farms, Empowering Futures
            </p>
            """,
            unsafe_allow_html=True
        )



# ---------------- ADMIN MODE ----------------
admin_mode = st.sidebar.toggle("🧑‍💼 Admin Simulation Mode", value=False)
st.session_state["admin_mode"] = admin_mode

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------
menu_items = [
    "Dashboard",
    "Find Storage",
    "Market Intelligence",
    "Services",
    "Profile",
    "Impact"
]

if admin_mode:
    menu_items.append("Admin Simulation")

menu = st.sidebar.radio("📍 Navigation", menu_items)

# ---------------- ROUTING ----------------
if menu == "Dashboard":
    dashboard.show()

elif menu == "Find Storage":
    storage.show()

elif menu == "Market Intelligence":
    market.show()

elif menu == "Services":
    services.show()

elif menu == "Profile":
    profile.show()

elif menu == "Impact":
    impact.show()

elif menu == "Admin Simulation":
    from views import admin_simulation
    admin_simulation.show()

st.set_page_config(page_title="Market Dashboard", layout="wide")

st.title("📊 Market Intelligence Dashboard")
st.caption("Interactive analytics powered by Google Looker Studio")

looker_studio_url = "https://lookerstudio.google.com/embed/reporting/733b387a-5772-4188-9f0a-341c1f7cf5dc/page/jjTlF"

components.iframe(
    src=looker_studio_url,
    width=1200,
    height=750
)

