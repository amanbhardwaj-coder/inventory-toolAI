import json
from datetime import datetime
import pandas as pd


def save_config(config, path):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    config["generated_at"] = datetime.utcnow().isoformat()

    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)



def create_normalized_file(df, config):

    rename = {}

    for item in config["mapping"]:

        if item["accepted_header"]:
            rename[
                item["vendor_column"]
            ] = item["accepted_header"]

    return df.rename(columns=rename)
