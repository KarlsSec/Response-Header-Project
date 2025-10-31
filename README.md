# Response-Header-Project
Automated Response Header Script made from the information at OWASP Secure Headers Project
https://owasp.org/www-project-secure-headers/

Made with Python 3.10.12

# Local
## how to run:
save burp response headers into <file.txt> 
python3 headers.py <file.txt> <csv_output_file>

Note: Clear-site-data is only valid on logout process. 

# Remote
## how to run:
python3 headers.py <url> <csv_output_file> --cookie="" (optional)

Note: Clear-site-data is only valid on logout process. 
