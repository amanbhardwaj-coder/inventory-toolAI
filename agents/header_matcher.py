import re

def norm(value):
    return re.sub(r"[^a-z0-9]", "", str(value).lower())

class HeaderMatcher:
    def __init__(self, knowledge):
        self.knowledge = knowledge

    def match(self, columns):
        results = {}
        for col in columns:
            best = None
            col_norm = norm(col)

            for setter, variations in self.knowledge.items():
                for variation in variations:
                    v_norm = norm(variation)

                    if col_norm == v_norm:
                        score = 1.0
                    elif col_norm in v_norm or v_norm in col_norm:
                        score = 0.8
                    else:
                        score = 0

                    if score and (not best or score > best["confidence"]):
                        best = {
                            "field": setter,
                            "confidence": score
                        }

            results[col] = best or {
                "field": "",
                "confidence": 0
            }

        return results
