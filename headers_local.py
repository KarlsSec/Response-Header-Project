#!/usr/bin/env python3
#Example usage: python3 headers.py target.txt
import sys # cli arg
import csv
import data_oct_2025


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 headers.py <file> <csv_output_file>")
        sys.exit(1)
    filename = sys.argv[1]
    csv_output_file = sys.argv[2]

# Parse the headers from the input file
    headers = parse_headers(filename)
# Get the expected headers from the data_oct_2025 module
    expected = data_oct_2025.expected


    
# Validate the headers and print the report
    report, missing_headers = validate_headers(headers, expected)
    print(report)
    # Get the header descriptions for the CSV
    
    csvoutput1 = get_header_description(missing_headers)
    csvoutput2 = get_header_recommendations(missing_headers)
    
    write_csv(csv_output_file + "_descriptions.csv", csvoutput1)
    write_csv(csv_output_file + "_recommendations.csv", csvoutput2)
    
    
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

