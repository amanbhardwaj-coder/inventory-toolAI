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

            accepted_header = variations[0]

            knowledge[setter] = {
                "accepted_header": accepted_header,
                "variations": variations,
            }

    return knowledge


def safe_dataframe_preview(df, rows=20):
    preview = df.head(rows).copy()
    preview.columns = [str(c).strip() for c in preview.columns]
    preview = preview.loc[:, ~preview.columns.duplicated()]
    st.dataframe(preview, use_container_width=True)


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
- Use description to identify jewelry type
- 14K metal prices should be 500 and the rest should be 1000
""",
)

if uploaded:

    if uploaded.name.lower().endswith(".xlsx"):
        df = pd.read_excel(uploaded, dtype=str, keep_default_na=False)
    else:
        df = pd.read_csv(uploaded, dtype=str, keep_default_na=False)

    st.subheader("File Preview")
    safe_dataframe_preview(df, 10)

    if st.button("Run AI Analysis"):

        agent = InventoryAgent(load_header_knowledge())

        config = agent.analyze(
            columns=list(df.columns),
            instructions=instructions,
        )

        st.session_state["config"] = config
        st.session_state["source_df"] = df


if "config" in st.session_state:

    st.subheader("AI Generated Mapping")

    config = st.session_state["config"]

    rows = []

    for item in config.get("mapping", []):
        rows.append({
            "Vendor Column": item.get("vendor_column", ""),
            "Accepted Header": item.get("accepted_header", ""),
            "Confidence": item.get("confidence", 0),
        })

    edited = st.data_editor(
        pd.DataFrame(rows),
        use_container_width=True,
        num_rows="fixed",
    )

    if st.button("Approve Mapping"):

        df = st.session_state.get("source_df")

        edited_rows = edited.to_dict("records")

        config["mapping"] = [
            {
                "vendor_column": row.get("Vendor Column", ""),
                "accepted_header": row.get("Accepted Header", ""),
                "confidence": row.get("Confidence", 0),
            }
            for row in edited_rows
        ]

        save_config(
            config,
            OUTPUT_DIR / "mapping_config.json",
        )

        normalized = create_normalized_file(
            df,
            config,
        )

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        normalized.to_csv(
            OUTPUT_DIR / "normalized_input.csv",
            index=False,
        )

        st.success("Mapping approved and normalized input created.")

        st.subheader("Normalized Input Preview")
        safe_dataframe_preview(normalized, 20)

        st.download_button(
            "Download normalized_input.csv",
            normalized.to_csv(index=False),
            "normalized_input.csv",
            mime="text/csv",
        )

        st.download_button(
            "Download mapping_config.json",
            (OUTPUT_DIR / "mapping_config.json").read_text(encoding="utf-8"),
            "mapping_config.json",
            mime="application/json",
        )
