from glob2 import glob


txt_files = glob('*.txt')

for txt_file in txt_files:
	f = open(txt_file, 'r', encoding='utf8')
	line = f.readline()
	f.close()
	data = line.split()
	for i in range(len(data)):
		if data[i].startswith('-'):
			x = int(data[i])
			new_width = int(data[i+2]) + x
			data[i] = str(0)
			data[i+2] = str(new_width)

	f = open(txt_file, 'w', encoding='utf8')
	write_line = ' '.join(data)
	f.write(write_line)
	f.truncate()
	f.close()

	print('Fixing file %s ..' % txt_file)

		

print('\nDone! ')
