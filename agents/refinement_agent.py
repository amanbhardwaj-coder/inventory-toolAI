class RefinementAgent:

    def normalize(self, value):

        if value is None:
            return ""

        value = str(value)
        value = value.replace("#", ",")
        value = value.replace("|", ",")
        value = value.replace(";", ",")

        values = []

        for x in value.split(","):
            x = x.strip()

            if x and x not in values:
                values.append(x)

        return ",".join(values)
