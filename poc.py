import os

x = list(range(10))
import time

# Introduce issues: busy wait, unused imports, and insecure temp file usage

def busy_wait(seconds):
	start = time.time()
	while time.time() - start < seconds:
		pass  # busy wait

def create_temp_file():
	fname = '/tmp/poc_temp.txt'
	f = open(fname, 'w')
	f.write('temp')
	return fname  # file not closed properly

def insecure_op():
	os.system('echo vulnerable')  # command injection risk if extended
