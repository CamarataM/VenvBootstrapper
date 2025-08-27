#!/usr/bin/env python3
import argparse
import sys
from venvbootstrapper import create_and_activate_virtualenv, add

def main():
	parser = argparse.ArgumentParser(prog='ImportTests', description='Tests the import location of the "mashumaro" module.')
	args = parser.parse_args()

	add('mashumaro')

	try:
		import mashumaro
		from mashumaro import DataClassDictMixin, MissingField, field_options
	except:
		raise AssertionError("mashumaro == None")

	try:
		assert DataClassDictMixin, "DataClassDictMixin == None"
	except:
		raise AssertionError("DataClassDictMixin == None")

	try:
		assert MissingField, "MissingField == None"
	except:
		raise AssertionError("MissingField == None")

	try:
		assert field_options, "field_options == None"
	except:
		raise AssertionError("field_options == None")

	print("Passed All Tests")

	return 0

if __name__ == '__main__':
	sys.exit(main())