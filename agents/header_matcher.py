import re


def norm(value):
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


class HeaderMatcher:

    def __init__(self, knowledge):
        self.knowledge = knowledge


    def match(self, columns):

        output = []

        for column in columns:

            best = {
                "vendor_column": column,
                "accepted_header": "",
                "internal_setter": "",
                "confidence": 0
            }

            for setter, data in self.knowledge.items():

                accepted = data["accepted_header"]

                for variation in data["variations"]:

                    score = 0

                    if norm(column) == norm(variation):
                        score = 1

                    elif norm(column) in norm(variation) or norm(variation) in norm(column):
                        score = 0.8

                    if score > best["confidence"]:
                        best = {
                            "vendor_column": column,
                            "accepted_header": accepted,
                            "internal_setter": setter,
                            "confidence": score
                        }

            output.append(best)

        return output
