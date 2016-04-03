import re

zip_re = re.compile(r'^\s*\d{5}$')
first_last_name_re = re.compile(r'^([A-Za-z]+\s*[A-Z]*\.*)\s+([A-Za-z]+)$')
last_first_name_re = re.compile(r'^([A-Za-z]+),\s+([A-Za-z]+)$')
phone_re = re.compile(r'^\s*\(\d{3}\)\-\d{3}\-\d{4}$|^\s*\d{3} \d{3} \d{4}$')
ssn_re = re.compile(r'^\d{3}[ -]{1}\d{2}[ -]{1}\d{4}$')
