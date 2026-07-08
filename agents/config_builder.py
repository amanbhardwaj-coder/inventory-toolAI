import json
from datetime import datetime

def build_config(mapping, inventory_type="unknown"):
    return {
        "inventory_type": inventory_type,
        "generated_at": datetime.utcnow().isoformat(),
        "mapping": mapping,
        "rules": {
            "variant_columns_only": True,
            "static_columns_preserved": True,
            "normalize_separators": True,
            "remove_duplicates": True
        }
    }

def save_config(config, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
