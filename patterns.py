import re

# Regex patterns for Indian PII
PHONE_PATTERN = re.compile(r'\b(\+91[\s-]?)?[6-9]\d{2}[\s-]?\d{3}[\s-]?\d{4}\b')
AADHAAR_PATTERN = re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b')
PAN_PATTERN = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b')
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-zA-Z]{2,}\b')
PIN_PATTERN = re.compile(r'\b\d{6}\b')
IP_PATTERN = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
URL_PATTERN = re.compile(r'https?://(?:www\.)?[^\s]+')
VEHICLE_PATTERN = re.compile(r'\b[A-Z]{2}[0-9]{1,2}[A-Z]{0,2}[0-9]{4}\b')
DATE_PATTERN = re.compile(r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2}|(?:\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December),?\s+\d{2,4})|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{2,4})\b')
ADDRESS_PATTERN = re.compile( r'\b((\d{1,4}\s)?[A-Za-z0-9\s\-/,]+(?:Street|St|Road|Rd|Avenue|Ave|Sector|Block|Lane|Colony|Nagar|Layout|Apartments|Society)[\s\d,/-]*)\b',re.IGNORECASE)