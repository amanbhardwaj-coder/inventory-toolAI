import streamlit as st
import pandas as pd
import json
from pathlib import Path

from agents.inventory_agent import InventoryAgent
from agents.config_builder import save_config

st.set_page_config(page_title="AI Inventory Platform", layout="wide")

HEADER_DIR = Path("configs/headers")
GENERATED_DIR = Path("configs/generated")

def load_headers():
    knowledge = {}
    for file in HEADER_DIR.glob("*.csv"):
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            setter = str(row.get("Setter name", "")).strip()
            values = str(row.get("Header variations", "")).split(",")
            knowledge.setdefault(setter, []).extend(
                [v.strip() for v in values if v.strip()]
            )
    return knowledge

st.title("AI Inventory Platform")

uploaded = st.file_uploader(
    "Upload vendor inventory",
    type=["csv", "xlsx"]
)

if uploaded:
    if uploaded.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded)
    else:
        df = pd.read_csv(uploaded)

    st.subheader("File Analysis")
    st.write({
        "rows": len(df),
        "columns": list(df.columns)
    })

    if st.button("Run AI Mapping"):
        agent = InventoryAgent(load_headers())
        config = agent.analyze(list(df.columns))

        st.session_state["config"] = config

    if "config" in st.session_state:
        st.subheader("AI Generated Mapping")

        config = st.session_state["config"]

        rows = []
        for col, value in config["mapping"].items():
            rows.append({
                "Vendor Column": col,
                "Target Field": value["field"],
                "Confidence": value["confidence"]
            })

        edited = st.data_editor(pd.DataFrame(rows), use_container_width=True)

        if st.button("Approve Mapping"):
            save_config(
                config,
                GENERATED_DIR / "mapping_config.json"
            )
            st.success("Mapping configuration saved.")
