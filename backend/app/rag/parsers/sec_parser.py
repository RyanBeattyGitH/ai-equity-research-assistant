from bs4 import BeautifulSoup
import re

class SECParser:

    def clean_text(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "lxml")
        text = soup.get_text(separator=" ")

        return text

    def extract_sections(self, text):
        sections = {}

        # Risk Factors
        risk = re.search(r"(?i)item 1a[\s\S]+?(?=item 1b|item 2)", text)
        if risk:
            sections["risk_factors"] = risk.group()

        # MD&A
        mda = re.search(r"(?i)item 7[\s\S]+?(?=item 7a|item 8)", text)
        if mda:
            sections["mda"] = mda.group()

        return sections
