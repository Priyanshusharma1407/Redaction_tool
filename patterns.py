import re

# Regex patterns for Indian PII
PHONE_PATTERN = re.compile(r'\b(?:\+91[\s\-]?)?\(?[6-9]\d{2}\)?[\s\-]?\d{3}[\s\-]?\d{4}\b')
AADHAAR_PATTERN = re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b')
PAN_PATTERN = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b')
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-zA-Z]{2,}\b')
PIN_PATTERN = re.compile(r'\b\d{6}\b')
IP_PATTERN = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
URL_PATTERN = re.compile(r'https?://(?:www\.)?[^\s]+')
VEHICLE_PATTERN = re.compile(r'\b[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}\b')
DATE_PATTERN = re.compile(
    r'\b(?:\d{1,2}(?:st|nd|rd|th)?[\s\-\/])?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|'
    r'Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t)?(?:ember)?|Oct(?:ober)?|'
    r'Nov(?:ember)?|Dec(?:ember)?)[\s\-\/]?\d{2,4}\b'  # e.g. 12 Aug 1995
    r'|\b\d{1,2}[\-\/]\d{1,2}[\-\/]\d{2,4}\b'          # e.g. 12/08/1995 or 08-12-1995
    r'|\b\d{4}[\-\/]\d{1,2}[\-\/]\d{1,2}\b',           # e.g. 1995-08-12
    re.IGNORECASE
)
ADDRESS_PATTERN = re.compile(
    r'\b(?:\d{1,4}\s)?(?:[A-Z]?[a-z]+\s){0,2}'
    r'(Street|St|Road|Rd|Avenue|Ave|Block|Sector|Nagar|Lane|Colony|Plaza|Society)\b',
    re.IGNORECASE
)
    


