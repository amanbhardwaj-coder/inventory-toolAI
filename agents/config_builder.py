import json
from datetime import datetime
import pandas as pd


def save_config(config, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    config["generated_at"] = datetime.utcnow().isoformat()

    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def _merge_series(existing, incoming):
    existing = existing.astype(str).fillna("")
    incoming = incoming.astype(str).fillna("")

    result = []

    for old, new in zip(existing.tolist(), incoming.tolist()):
        old = "" if old.lower() == "nan" else old
        new = "" if new.lower() == "nan" else new

        if old.strip() and new.strip() and old.strip() != new.strip():
            result.append(f"{old},{new}")
        elif old.strip():
            result.append(old)
        else:
            result.append(new)

    return pd.Series(result)


def create_normalized_file(df, config):

    rename = {}

    for item in config.get("mapping", []):

        vendor_column = (
            item.get("vendor_column")
            or item.get("Vendor Column")
        )

        accepted_header = (
            item.get("accepted_header")
            or item.get("Accepted Header")
        )

        if vendor_column and accepted_header:
            rename[vendor_column] = accepted_header


    normalized = df.rename(columns=rename)


    # Merge duplicate columns created by AI mapping
    if normalized.columns.duplicated().any():

        merged = {}

        for column in normalized.columns:

            if column not in merged:
                merged[column] = normalized[column]
            else:
                merged[column] = _merge_series(
                    merged[column],
                    normalized[column]
                )

        normalized = pd.DataFrame(merged)


    normalized.columns = [
        str(col).strip()
        for col in normalized.columns
    ]

    return normalized
