import re
import patterns
import spacy
from collections import namedtuple

nlp = spacy.load("en_core_web_md")

Match = namedtuple("Match", ["start", "end", "label", "text"])

# Mapping for spaCy NER labels to consistent REDACTED tags
NER_LABEL_MAP = {
    "PERSON": "PERSON",
    "ORG": "ORG",
    "GPE": "LOCATION",
}

def get_regex_matches(text):
    matches = []
    regex_patterns = {
        "PHONE": patterns.PHONE_PATTERN,
        "AADHAAR": patterns.AADHAAR_PATTERN,
        "PAN": patterns.PAN_PATTERN,
        "EMAIL": patterns.EMAIL_PATTERN,
        "PINCODE": patterns.PIN_PATTERN,
        "ADDRESS": patterns.ADDRESS_PATTERN,
        "IP": patterns.IP_PATTERN,
        "URL": patterns.URL_PATTERN,
        "VEHICLE": patterns.VEHICLE_PATTERN,
        "DATE": patterns.DATE_PATTERN,  
    }
    for label, pattern in regex_patterns.items():
        for match in pattern.finditer(text):
            matches.append(Match(match.start(), match.end(), label, match.group()))
    return matches

def get_ner_matches(text):
    matches = []
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in NER_LABEL_MAP:
            norm_label = NER_LABEL_MAP[ent.label_]
            matches.append(Match(ent.start_char, ent.end_char, norm_label, ent.text))
    return matches

def remove_overlapping_matches(matches):
    """Remove overlapping matches and keep longest first."""
    seen = set()
    result = []
    for match in sorted(matches, key=lambda m: (m.start, -m.end)):
        if not any(match.start < s[1] and match.end > s[0] for s in seen):
            result.append(match)
            seen.add((match.start, match.end))
    return result


def redact_all(text):
    all_matches = get_regex_matches(text) + get_ner_matches(text)
    non_overlapping = remove_overlapping_matches(all_matches)

    # Redact from end to start to preserve indexes
    non_overlapping.sort(key=lambda m: m.start, reverse=True)

    for match in non_overlapping:
        placeholder = f"[REDACTED_{match.label}]"
        text = text[:match.start] + placeholder + text[match.end:]

    return text
