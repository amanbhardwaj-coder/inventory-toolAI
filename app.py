import streamlit as st
import pandas as pd
from pathlib import Path

from agents.inventory_agent import InventoryAgent
from agents.config_builder import save_config, create_normalized_file

HEADER_DIR = Path("configs/headers")
OUTPUT_DIR = Path("configs/generated")

st.set_page_config(page_title="AI Inventory Agent", layout="wide")

def load_header_knowledge():
    knowledge = {}

    for file in HEADER_DIR.glob("*.csv"):
        df = pd.read_csv(file)

        for _, row in df.iterrows():
            setter = str(row.get("Setter name", "")).strip()
            variations = [
                x.strip()
                for x in str(row.get("Header variations", "")).split(",")
                if x.strip()
            ]

            if not setter or not variations:
                continue

            # first variation is treated as accepted display header
            accepted_header = variations[0]

            knowledge[setter] = {
                "accepted_header": accepted_header,
                "variations": variations
            }

    return knowledge


st.title("AI Inventory Agent")

uploaded = st.file_uploader(
    "Upload Vendor Inventory",
    type=["csv", "xlsx"]
)

instructions = st.text_area(
    "AI Instructions",
    placeholder="""
Example:
- Convert metal values into Available Metals
- Keep Jewelry Style static
- Create variants only for metal and shape
- Use description to detect jewelry type
"""
)

if uploaded:

    if uploaded.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded)
    else:
        df = pd.read_csv(uploaded)

    st.subheader("File Preview")
    st.dataframe(df.head(10))

    if st.button("Run AI Analysis"):

        agent = InventoryAgent(
            load_header_knowledge()
        )

        config = agent.analyze(
            columns=list(df.columns),
            instructions=instructions
        )

        st.session_state["config"] = config


if "config" in st.session_state:

    st.subheader("AI Generated Mapping")

    config = st.session_state["config"]

    rows = []

    for item in config["mapping"]:
        rows.append({
            "Vendor Column": item["vendor_column"],
            "Accepted Header": item["accepted_header"],
            "Confidence": item["confidence"]
        })

    edited = st.data_editor(
        pd.DataFrame(rows),
        use_container_width=True
    )

    if st.button("Approve Mapping"):

        config["mapping"] = edited.to_dict("records")

        save_config(
            config,
            OUTPUT_DIR / "mapping_config.json"
        )

        normalized = create_normalized_file(
            df,
            config
        )

        normalized.to_csv(
            OUTPUT_DIR / "normalized_input.csv",
            index=False
        )

        st.success("Mapping approved and normalized input created.")

        st.subheader("Normalized Input Preview")
        st.dataframe(normalized.head(20))

        st.download_button(
            "Download normalized_input.csv",
            normalized.to_csv(index=False),
            "normalized_input.csv"
        )
