import re
import pandas as pd


def get_language_from_text(text):
    code_pattern = re.compile(r'(?<=\<code\>)(.+?)(?=\</code\>)', re.DOTALL)
    matches = re.findall(code_pattern, text)
    return '\n'.join(matches)