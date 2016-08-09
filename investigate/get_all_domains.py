# Simple script to get all domains associated with an email
# To run: python get_all_domains.py [email] [/path/to/api_key]
# Example: python get_all_domains.py hello@yahoo.com /keys/api_key.txt
# Make sure api_key file is just one line that contains API key
# Results are saved to domains-[email]

import investigate
import sys
from pprint import pprint

try:
	email = sys.argv[1]
	path = sys.argv[2]
except IndexError:
	print('Please enter an email & path to a file containing your Investigate API key')
	sys.exit(1)
try:
	api_key = open(path, 'r').read()
except IOError:
	print('Could not find file: {0}'.format(path))
	sys.exit(1)

# Parameters for querying
offset, inc = 0, 500
more_data = True
domains = []
inv = investigate.Investigate(api_key)

while more_data:
	response = inv.email_whois(email, offset)
	hits = response[email]['domains']
	for i in range(len(hits)):
		domains.append(hits[i]['domain'])
	more_data = response[email]['moreDataAvailable']
	offset += inc

domains = set(domains)

with open('domains-{0}'.format(email), 'w') as result:
	[result.write(domain+'\n') for domain in domains]