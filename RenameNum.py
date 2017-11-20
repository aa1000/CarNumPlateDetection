from glob2 import glob
from os import rename
from platform import platform

name_seed = input('Enter name seed: ')

txt_files = glob('*.txt')

for txt_file in txt_files:
	#txt_split = txt_file.split('.')
	#if len(txt_split[0]) < 1:
	f = open(txt_file, 'r', encoding='utf8')
	line = f.readline()
	f.close()
	data = line.split()
	data[0] = name_seed + data[0]
	f = open(txt_file, 'w', encoding='utf8')
	write_line = ' '.join(data)
	f.write(write_line)
	f.truncate()
	f.close()

	new_txt_name = name_seed + txt_file
	print('\nChanging file %s name to %s ..' % (txt_file, new_txt_name))
	rename(txt_file, new_txt_name)

		


img_files = glob('*.JPG')
img_files.extend(glob('*.JPEG'))

# windows is case insensitive so we don't need to add this
if not platform().startswith('Windows'):
    img_files.extend(glob('*.jpg'))
    img_files.extend(glob('*.jpeg'))

for img_file in img_files:
	#img_split = img_file.split()
	#if len(img_split[0]) < 1:
	new_img_name = name_seed + img_file
	print('\nChanging image %s name to %s ..' % (img_file, new_img_name))
	rename(img_file, ''.join(new_img_name))

print('Done! ')
