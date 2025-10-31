#!/usr/bin/env python3
#Example usage: python3 headers_remote.py <url> <csv_output_file> [--cookie "cookie_string"] 
# if using cookie flag make sure WAF is disabled for accurate results
import sys # cli arg
import csv
import data_oct_2025
import requests
import argparse
requests.packages.urllib3.disable_warnings()

# Turn off requests internal logging
import logging
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

def main():
    parser = argparse.ArgumentParser(description="Fetch HTTP headers from a URL and validate them against expected security headers.")
    
    #required url argument
    parser.add_argument("url", help="The URL to fetch headers from.")
    #optional csv output file argument
    parser.add_argument(
        'csv_output_file',
        nargs='?',
        default='report.csv',
        help="The base name for the CSV output files (default: report.csv)."
    )
    #optinal cookie argument
    parser.add_argument(
        '--cookie',
        type=str,
        default=None,
        help="Optional cookie string to include in the request. (e.g., \"sessionid=abc123\")"
    )
    #parse arguments
    args = parser.parse_args()
    url = args.url
    csv_output_file = args.csv_output_file
    cookie = args.cookie
        
# Make HTTP request to get headers
    response_headers = httpquery(url, cookie)
    
# Get the expected headers from the data_oct_2025 module
    expected = data_oct_2025.expected
    
# Validate the headers and print the report
    report, missing_headers = validate_headers(response_headers, expected)
    print(report)
    
    

# csv output for missing headers
    csvoutput1 = get_header_description(missing_headers)
    csvoutput2 = get_header_recommendations(missing_headers)
    
    write_csv(csv_output_file + "_descriptions.csv", csvoutput1)
    write_csv(csv_output_file + "_recommendations.csv", csvoutput2)

#get only the header descriptions for the missing headers
def httpquery(url, cookie=None):
    request_headers = {'Cookie': cookie} if cookie else {}
    striped_headers = []
    try:
        response = requests.get(url, headers=request_headers)
    except requests.RequestException as e:
            print(f"Error fetching URL {url} with cookie: {e}")
            sys.exit(1)
    
    for key, _ in response.headers.items():
        lowered_key = key.lower().strip()
        striped_headers.append(lowered_key)
    return striped_headers

def validate_headers(headers, expected):

    issues = []
    missing = []

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
            missing.append(key)
            #list to store missing headers for other uses
            
        elif exp_val is not None and headers.get(key_l) != exp_val:
            issues.append(f"MISMATCH {key}: got '{headers.get(key_l)}', expected '{exp_val}'")

    if issues:
        report = f"FAIL: {', '.join(issues)}\nFull headers: {headers}" 
    else:
        report = "PASS: All expected headers match."
    return report, missing


def get_header_description(headers):
    headerdesc = ["Header, Description"]
    for x in headers:
        col2 =  data_oct_2025.secure_headers.get(x, "Description not found.")
        col1 = x
        headerdesc.append(f"{col1}, {col2}")
    return headerdesc
 

def get_header_recommendations(headers):
    recommendations = ["Header, Example"]
    for x in headers:
        col2 =  data_oct_2025.secure_header_examples.get(x, "No example available.")
        col1 = x
        recommendations.append(f"{col1}, {col2}")
    return recommendations

def write_csv(filename, data):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for line in data:
            parts = line.split(', ', 1)  # [header, rest_of_desc]
            if len(parts) == 2:
                writer.writerow(parts)
            else:
                writer.writerow([line])  # fallback

if __name__ == "__main__":
    main()