# coding: utf8

import os,sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from parse import *

def test_nt(nt_fun, input_file, should_halt):
	global line_no, column_no
	test_fail=False
	try:
		print("testing " + nt_fun.__name__ + " with input " + input_file )
		open_symbolic_file(input_file)
		read_one_symbol()
		nt_fun()
		if not should_halt:
			print("SUCCESS: " + nt_fun.__name__ + " succeeded as expected")
		else:
			test_fail=True
			print("FAIL: " + nt_fun.__name__ + " didn't halt as expected")
	except SystemExit:
		if should_halt:
			print("SUCCESS: " + nt_fun.__name__ + " halted as expected")
		else:
			test_fail=True
			print("FAIL: " + nt_fun.__name__ + " halted incorrectly")
	except Exception as e:
		print('Exception: ')
		print(e)
		test_fail=True
	print()
	return test_fail

def accepta(): accept('a')
def acceptb(): accept('b')

tests = [
	(accepta, 'input-files/identifier_1', False),
	(acceptb, 'input-files/identifier_1', True),
	(nt_identifier, 'input-files/identifier_1', False),
	(nt_identifier, 'input-files/identifier_2', False),
	(nt_identifier, 'input-files/identifier_3', False),
	(nt_identifier, 'input-files/identifier_4', False),
]

def main():
	num_fail = 0
	num_succ = 0
	for nt_fun, input_file, should_halt in tests:
		test_fail = test_nt(nt_fun, input_file, should_halt)
		if test_fail:
			num_fail += 1
		else:
			num_succ += 1

	print(num_fail, "tests failed, ", num_succ, "tests succeeded")

if __name__ == "__main__":
	main()