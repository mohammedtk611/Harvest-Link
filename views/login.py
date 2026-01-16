import streamlit as st
import pandas as pd
from pathlib import Path

DATA = Path("data")

def show():
    st.title("🔐 Login to HarvestLink")

    users = pd.read_csv(DATA / "users.csv")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = users[
            (users["username"] == username) &
            (users["password"] == password)
        ]

        if user.empty:
            st.error("Invalid credentials")
            return

        user = user.iloc[0]
        st.session_state["logged_in"] = True
        st.session_state["role"] = user["role"]
        st.session_state["linked_id"] = user["linked_id"]

        st.success(f"Logged in as {user['role']}")
        st.rerun()
