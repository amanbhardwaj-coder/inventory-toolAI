import re


def parse_english_rules(instructions: str):
    """
    Lightweight English-to-rule parser.

    This is intentionally deterministic for V3 foundation.
    Later it can be replaced/augmented with a real LLM call.
    """
    text = (instructions or "").lower()
    rules = {
        "pricing_rules": [],
        "normalization_rules": [],
        "variant_rules": [],
    }

    # Example:
    # "14k metal prices should be 500 and rest should be 1000"
    if "14k" in text:
        prices = [float(x) for x in re.findall(r"\b\d+(?:\.\d+)?\b", text)]
        if len(prices) >= 2:
            rules["pricing_rules"].append(
                {
                    "type": "metal_contains",
                    "contains": "14k",
                    "price": prices[0],
                    "default_price": prices[1],
                }
            )

    if "only" in text and "metal" in text:
        rules["variant_rules"].append({"expand_only_mentions": True})

    if "duplicate" in text or "duplicates" in text:
        rules["normalization_rules"].append({"remove_duplicates": True})

    if "#" in instructions or "separator" in text:
        rules["normalization_rules"].append({"normalize_separators": True})

    return rules
