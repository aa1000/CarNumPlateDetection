from glob2 import glob


txt_files = glob('*.txt')

for txt_file in txt_files:
	f = open(txt_file, 'r', encoding='utf8')
	line = f.readline()
	f.close()
	data = line.split()
	for i in range(1, 5):
		j = i +4
		data[i], data[j] = data[j], data[i]
	#data[2], data[6] = data[], data[6]
	#data[1], data[2] = data[5], data[6]
	#data[1], data[2] = data[5], data[6]
	f = open(txt_file, 'w', encoding='utf8')
	write_line = ' '.join(data)
	f.write(write_line)
	f.truncate()
	f.close()

	print('Fixing file %s ..' % txt_file)

		

print('\nDone! ')
