#Cleans Spaces in file names becuase they cause problems with splitting strings
from glob2 import glob
from os import rename
from platform import platform

txt_files = glob('*.txt')

def isgdig(check_str):
	try:
		int(check_str)
		return True
	except ValueError:
		return  False

for txt_file in txt_files:
	txt_split = txt_file.split()
	if len(txt_split) > 1:
		f = open(txt_file, 'r', encoding='utf8')
		line = f.readline()
		f.close()
		data = line.split()
		for i in range(len(data)-1):
			if data[i].find('.') > 0 and isgdig(data[i+1]):
				new_name = data[0:i+1]
				data[i] = ''.join(new_name)
				data = data[i:]
				f = open(txt_file, 'w', encoding='utf8')
				write_line = ' '.join(data)
				f.write(write_line)
				f.truncate()
				f.close()
				break
		new_txt_name = ''.join(txt_split)
		print('\nChanging file %s name to %s ..' % (txt_file, new_txt_name))
		rename(txt_file, new_txt_name)

		

#get all jpg image files
img_files = glob('*.JPG')
img_files.extend(glob('*.JPEG'))

# windows is case insensitive so we don't need to add this
if not platform().startswith('Windows'):
    img_files.extend(glob('*.jpg'))
    img_files.extend(glob('*.jpeg'))

#Change the names of the image files
for img_file in img_files:
	img_split = img_file.split()
	if len(img_split) > 1:
		new_img_name = ''.join(img_split)
		print('\nChanging image %s name to %s ..' % (img_file, new_img_name))
		rename(img_file, ''.join(new_img_name))

print('Done! ')
