import os, os.path
from glob import glob

file_path = input('enter text file path: ')

with open(file_path) as f:
	for line in f:
		line = line.rstrip('\n')
		if os.path.isfile(line):
			os.remove(line)
			print('Deleting ' + line)
			text_name = line.split('.')[0] + '.txt'
			if os.path.isfile(text_name):
				os.remove(text_name)
				print('Deleting ' + text_name)
		else:
			print('Found Nothing')
