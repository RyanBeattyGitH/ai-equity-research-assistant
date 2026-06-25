import re


def detect_section(text: str) -> str:

    text_upper = text.upper()

    if "ITEM 1A" in text_upper:
        return "risk_factors"

    if "ITEM 7" in text_upper:
        return "mdna"

    return "other"
