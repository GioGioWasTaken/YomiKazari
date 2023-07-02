from deinflector_data import data

class Deinflector:
    def __init__(self, reasons):
        self.reasons = Deinflector.normalize_reasons(reasons)

    def deinflect(self, source):
        results = [self.create_deinflection(source, 0, [])]
        for i in range(len(results)):
            rules, term, reasons = results[i]["rules"], results[i]["term"], results[i]["reasons"]
            for reason, variants in self.reasons:
                for kanaIn, kanaOut, rulesIn, rulesOut in variants:
                    if (
                        (rules != 0 and (rules & rulesIn) == 0) or
                        not term.endswith(kanaIn) or
                        (len(term) - len(kanaIn) + len(kanaOut)) <= 0
                    ):
                        continue

                    results.append(
                        self.create_deinflection(
                            term[:len(term) - len(kanaIn)] + kanaOut,
                            rulesOut,
                            [reason] + reasons
                        )
                    )
        return results

    def create_deinflection(self, term, rules, reasons):
        return {"term": term, "rules": rules, "reasons": reasons}

    @staticmethod
    def normalize_reasons(reasons):
        normalized_reasons = []
        for reason, reason_info in reasons.items():
            variants = []
            for variant in reason_info:
                kanaIn = variant["kanaIn"]
                kanaOut = variant["kanaOut"]
                rulesIn = Deinflector.rules_to_rule_flags(variant["rulesIn"])
                rulesOut = Deinflector.rules_to_rule_flags(variant["rulesOut"])
                variants.append([kanaIn, kanaOut, rulesIn, rulesOut])
            normalized_reasons.append([reason, variants])
        return normalized_reasons

    @staticmethod
    def rules_to_rule_flags(rules):
        rule_types = {
            "v1":    0b00000001,  # Verb ichidan
            "v5":    0b00000010,  # Verb godan
            "vs":    0b00000100,  # Verb suru
            "vk":    0b00001000,  # Verb kuru
            "vz":    0b00010000,  # Verb zuru
            "adj-i": 0b00100000,  # Adjective i
            "iru":   0b01000000   # Intermediate -iru endings for progressive or perfect tense
        }
        value = 0
        for rule in rules:
            rule_bits = rule_types.get(rule)
            if rule_bits is None:
                continue
            value |= rule_bits
        return value
deinflector_object=Deinflector(data)
print(deinflector_object.deinflect("堪らない"))