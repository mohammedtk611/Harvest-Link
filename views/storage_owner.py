import streamlit as st
import pandas as pd
from pathlib import Path

DATA = Path("data")

def show():
    st.title("🏬 Storage Owner Dashboard")

    storage = pd.read_csv(DATA / "cold_storage.csv")
    storage_id = int(st.session_state["linked_id"])

    my_storage = storage[storage["storage_id"] == storage_id].iloc[0]

    st.subheader(my_storage["storage_name"])
    st.write(f"City: {my_storage['city']}")

    new_available = st.number_input(
        "Update Available Tons",
        min_value=0.0,
        max_value=float(my_storage["capacity_tons"]),
        value=float(my_storage["available_tons"])
    )

    if st.button("Update Availability"):
        storage.loc[
            storage["storage_id"] == storage_id,
            "available_tons"
        ] = new_available

        storage.to_csv(DATA / "cold_storage.csv", index=False)
        st.success("Availability updated successfully")
