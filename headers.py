#!/usr/bin/env python3
#Example usage: python3 headers.py target.txt
import sys # cli arg


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 headers.py <file>")
        sys.exit(1)
    filename = sys.argv[1]
    
    
    headers = parse_headers(filename)
    
    expected = {
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Content-Security-Policy",
        "X-Permitted-Cross-Domain-Policies",
        "Referrer-Policy",
        "Clear-Site-Data",
        "Cross-Origin-Embedder-Policy",
        "Cross-Origin-Opener-Policy",
        "Cross-Origin-Resource-Policy",
        "Cache-Control",
        "X-DNS-Prefetch-Control"
    }

    report = validate_headers(headers, expected)
    print(report)
    
def parse_headers(filename):
    headers = {}
    with open(filename, 'r') as file:
        lines = []
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                break
            if line_num == 1:
                print(f"Status Line: {line}")
                continue
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key.lower().strip()] = value.strip()
    return headers
        
def validate_headers(headers, expected):
    """Check presence and optional expected values, return report string.

    `expected` may be either:
      - an iterable (set/list/tuple) of header names to check for presence, or
      - a dict mapping header names to expected values (use None for presence-only).

    Header name matching is case-insensitive.
    """
    issues = []

    # If expected is a dict, iterate items; otherwise treat entries as name->None
    if isinstance(expected, dict):
        items = expected.items()
    else:
        items = ((name, None) for name in expected)

    for key, exp_val in items:
        key_l = key.lower()
        # headers keys are stored lower-cased by parse_headers
        if key_l not in headers:
            issues.append(f"MISSING: {key}")
        elif exp_val is not None and headers.get(key_l) != exp_val:
            issues.append(f"MISMATCH {key}: got '{headers.get(key_l)}', expected '{exp_val}'")

    if issues:
        return f"FAIL: {', '.join(issues)}\nFull headers: {headers}"
    return "PASS: All expected headers match."

if __name__ == "__main__":
    main()