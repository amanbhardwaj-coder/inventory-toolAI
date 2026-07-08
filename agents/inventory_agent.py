from agents.header_matcher import HeaderMatcher


class InventoryAgent:

    def __init__(self, knowledge):
        self.matcher = HeaderMatcher(knowledge)

    def analyze(self, columns, instructions=""):

        return {
            "instructions": instructions,
            "mapping": self.matcher.match(columns)
        }
