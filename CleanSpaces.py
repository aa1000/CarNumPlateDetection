from glob2 import glob
from os import rename
from platform import platform

txt_files = glob('*.txt')

for txt_file in txt_files:
	txt_split = txt_file.split()
	if len(txt_split) > 1:
		f = open(txt_file, 'r', encoding='utf8')
		line = f.readline()
		f.close()
		data = line.split()
		for i in range(len(data)-1):
			#print(txt_file)
			#print(data[i], data[i+1])
			if data[i].find('.') > 0 and data[i+1].isdigit():
				new_name = data[0:i+1]
				data[i] = ''.join(new_name)
				data = data[i:]
				f = open(txt_file, 'w', encoding='utf8')
				write_line = ' '.join(data)
				f.write(write_line)
				f.truncate()
				f.close()
				break
				#for j in range(1, i):
				#	data.remove(data[j])
		new_txt_name = ''.join(txt_split)
		print('\nChanging file %s name to %s ..' % (txt_file, new_txt_name))
		rename(txt_file, new_txt_name)

		


img_files = glob('*.JPG')
img_files.extend(glob('*.JPEG'))

# windows is case insensitive so we don't need to add this
if not platform().startswith('Windows'):
    img_files.extend(glob('*.jpg'))
    img_files.extend(glob('*.jpeg'))

for img_file in img_files:
	img_split = img_file.split()
	if len(img_split) > 1:
		new_img_name = ''.join(img_split)
		print('\nChanging image %s name to %s ..' % (img_file, new_img_name))
		rename(img_file, ''.join(new_img_name))

print('Done! ')
