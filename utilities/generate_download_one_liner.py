#!/usr/bin/env python3
import http.client
import json
from pathlib import Path
import sys
from typing import Dict, List
from html.parser import HTMLParser

def main():
	download_bootstrapper_lines : List[str] = []
	with open(Path('venvbootstrapper/venvbootstrapper.py'), 'r', encoding='utf-8') as venvbootstrapper_file:
		in_download_bootstrapper_function = False
		for line in venvbootstrapper_file.readlines():
			if line.strip().startswith('#'):
				continue

			if in_download_bootstrapper_function:
				if line.startswith('\t'):
					download_bootstrapper_lines.append(line)
				else:
					in_download_bootstrapper_function = False

			if not in_download_bootstrapper_function and len(download_bootstrapper_lines) > 0:
				break

			if line.startswith('def download_venvbootstrapper'):
				in_download_bootstrapper_function = True

	download_bootstrapper_lines_string = ''.join([download_bootstrapper_line.strip('\t') for download_bootstrapper_line in download_bootstrapper_lines])

	https_connection = http.client.HTTPSConnection('flatliner.herokuapp.com')
	https_connection.request(
		'POST',
		'/',
		json.dumps({
			'text': download_bootstrapper_lines_string
		})
	)

	response = https_connection.getresponse()
	response_data : Dict[str, str] = json.loads(response.read().decode())

	download_bootstrapper_oneliner_text : str | None = response_data.get('text', None)
	print(download_bootstrapper_oneliner_text)

	download_bootstrapper_oneliner_links_text : str | None = response_data.get('links', None)
	if download_bootstrapper_oneliner_links_text != None:
		class DeleteURLHTMLParser(HTMLParser):
			def handle_starttag(self, tag, attrs):
				if tag == 'a':
					for attr in attrs:
						key = attr[0]
						value = attr[1]

						if 'delete' in value:
							https_connection.request('GET', value.removeprefix(f"https://{https_connection.host}"))
							break

		DeleteURLHTMLParser().feed(download_bootstrapper_oneliner_links_text)

	return 0

if __name__ == '__main__':
	sys.exit(main())