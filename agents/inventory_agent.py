from .header_matcher import HeaderMatcher
from .refinement_agent import RefinementAgent
from .config_builder import build_config

class InventoryAgent:

    def __init__(self, header_knowledge):
        self.matcher = HeaderMatcher(header_knowledge)
        self.refiner = RefinementAgent()

    def analyze(self, columns):
        mapping = self.matcher.match(columns)

        return build_config(
            mapping=mapping,
            inventory_type=self.detect_type(mapping)
        )

    def detect_type(self, mapping):
        fields = [
            x.get("field","")
            for x in mapping.values()
        ]

        if any("diamond" in x.lower() for x in fields):
            return "diamond"

        if any("jewelry" in x.lower() for x in fields):
            return "jewelry"

        return "unknown"
