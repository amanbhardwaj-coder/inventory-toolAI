import re

class RefinementAgent:

    def normalize_value(self, value):
        if value is None:
            return ""

        value = str(value).strip()
        value = value.replace("#", ",")
        value = value.replace("|", ",")
        value = value.replace(";", ",")

        value = re.sub(r"\s*,\s*", ",", value)

        tokens = []
        for x in value.split(","):
            x = x.strip()
            if x and x not in tokens:
                tokens.append(x)

        return ",".join(tokens)

    def refine(self, row, variant_columns):
        output = {}

        for key, value in row.items():
            if key in variant_columns:
                output[key] = self.normalize_value(value)
            else:
                output[key] = value

        return output
