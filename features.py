import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = ['login', 'verify', 'update', 'banking', 'secure', 'signin', 'account', 'ebayisapi', 'paypal', 'webscr', 'confirm', 'password', 'wallet', 'free', 'bonus']
SUSPICIOUS_TLDS = ['.xyz', '.top', '.tk', '.ml', '.ga', '.cf', '.gq', '.icu', '.club', '.work']

def extract_features_from_url(url: str):
    url_str = str(url).strip()
    if not url_str.startswith(('http://', 'https://')):
        url_parsed = urlparse('http://' + url_str)
    else:
        url_parsed = urlparse(url_str)

    hostname = url_parsed.netloc.lower()
    full_url = url_str.lower()

    # Length features
    url_len = len(full_url)
    hostname_len = len(hostname)

    # Character count features
    dots = full_url.count('.')
    hyphens = full_url.count('-')
    at_symbol = full_url.count('@')
    question_mark = full_url.count('?')
    equal_sign = full_url.count('=')
    slash_count = full_url.count('/')
    digits_count = sum(c.isdigit() for c in full_url)

    # Specific security checks
    has_ip = 1 if re.search(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', hostname) else 0
    is_https = 1 if url_parsed.scheme == 'https' else 0
    suspicious_count = sum(1 for word in SUSPICIOUS_WORDS if word in full_url)
    has_bad_tld = 1 if any(hostname.endswith(tld) for tld in SUSPICIOUS_TLDS) else 0

    return [
        url_len,
        hostname_len,
        dots,
        hyphens,
        at_symbol,
        question_mark,
        equal_sign,
        slash_count,
        digits_count,
        has_ip,
        is_https,
        suspicious_count,
        has_bad_tld
    ]