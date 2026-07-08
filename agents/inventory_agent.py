from agents.header_matcher import HeaderMatcher


class InventoryAgent:

    def __init__(self, knowledge):
        self.matcher = HeaderMatcher(knowledge)


    def analyze(self, columns, instructions=""):

        return {
            "instructions": instructions,
            "mapping": self.matcher.match(columns),
            "ai_rules": self.parse_business_rules(instructions)
        }


    def parse_business_rules(self, instructions):

        text = (instructions or "").lower()

        rules = {}

        if "14k" in text and "500" in text:
            rules["metal_price_rule"] = {
                "14k": 500,
                "default": 1000
            }

        return rules
