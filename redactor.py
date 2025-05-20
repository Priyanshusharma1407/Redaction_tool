import re
import spacy
from collections import namedtuple, Counter
from transformers import pipeline
import patterns

nlp = spacy.load("en_core_web_md")
ner_pipeline = pipeline("ner", grouped_entities=True, model="dslim/bert-base-NER")

Match = namedtuple("Match", ["start", "end", "label", "text"])

NER_LABEL_MAP = {
    "PERSON": "PERSON",
    "ORG": "ORG",
    "GPE": "LOCATION",
}
HF_LABEL_MAP = {
    "PER": "PERSON",
    "ORG": "ORG",
    "LOC": "LOCATION",
}

DENY_NER_TERMS = {"scooter", "car", "ambulance", "bike", "vehicle", "truck"}
SAFE_WORDS = {"pii", "json", "data", "text", "mapping", "summary", "case", "field"}

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

def get_spacy_ner_matches(text):
    matches = []
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in NER_LABEL_MAP:
            if ent.text.lower() in DENY_NER_TERMS:
                continue
            norm_label = NER_LABEL_MAP[ent.label_]
            matches.append(Match(ent.start_char, ent.end_char, norm_label, ent.text))
    return matches

def get_hf_ner_matches(text):
    matches = []
    for ent in ner_pipeline(text):
        label = HF_LABEL_MAP.get(ent['entity_group'], None)
        if not label:
            continue
        segment = text[ent['start']:ent['end']]
        if segment.lower() in DENY_NER_TERMS:
            continue
        matches.append(Match(ent['start'], ent['end'], label, segment))
    return matches

def remove_overlapping_matches(matches):
    seen = set()
    result = []
    for match in sorted(matches, key=lambda m: (m.start, -m.end)):
        if not any(match.start < e and match.end > s for s, e in seen):
            result.append(match)
            seen.add((match.start, match.end))
    return result

def merge_duplicate_entities(matches):
    seen_texts = set()
    deduped = []
    for m in matches:
        key = m.text.strip().lower()
        if key not in seen_texts:
            seen_texts.add(key)
            deduped.append(m)
    return deduped

# Redaction function
def redact_all(text):
    regex_matches = get_regex_matches(text)
    spacy_matches = get_spacy_ner_matches(text)
    # hf_matches = get_hf_ner_matches(text)

    all_matches = regex_matches + spacy_matches 
    all_matches = remove_overlapping_matches(all_matches)
    all_matches = merge_duplicate_entities(all_matches)
    all_matches.sort(key=lambda m: m.start, reverse=True)

    redacted_text = text
    protected_ranges = []
    mapping_log = []

    for match in all_matches:
        segment = redacted_text[match.start:match.end].strip()
        if segment.startswith("[REDACTED_") or segment.lower() in SAFE_WORDS:
            continue

        placeholder = f"[REDACTED_{match.label}]"
        redacted_text = redacted_text[:match.start] + placeholder + redacted_text[match.end:]
        protected_ranges.append((match.start, match.start + len(placeholder)))
        mapping_log.append((match.label, match.text))

    summary = dict(Counter(label for label, _ in mapping_log))
    return redacted_text, mapping_log, summary
