import sys, argparse, cv2, time
from glob2 import glob
import os, os.path
from shutil import copy as fcopy
from platform import platform

# delay for swapping between pics automatically
swap_delay = None

# hight of the image window
newHeight = None

# speed-up opencv using multithreads
cv2.setUseOptimized(True);
cv2.setNumThreads(8);

#parser = argparse.ArgumentParser(description='Checks the image data for faults, copies the correct data into a new folder then displays the correct image.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')

#args = parser.parse_args()

	

def CheckIfNumeric(list):
	for i in range(1, 9):
		if not list[i].isdigit():
			return False
	return True


folders_path = os.path.realpath('') + '/'

folders = glob(folders_path + '*/')

#clean the list from any files
for folder in folders:
	if not folder.endswith('/') or folder.endswith('Output/'):
		folders.remove(folder)


if not os.path.isdir(folders_path+ 'Output'):
	#make a folder to copy the files into it
	os.mkdir(folders_path + 'Output')

for folder in folders:
	files_path = folder
	print('\nFolder: ' + files_path)

	txt_files = glob(files_path + '*.txt')
	img_files = glob(files_path + '*.JPG')
	img_files.extend(glob(files_path + '*.JPEG'))
	

	# windows is case insensitive so we don't need to add this
	if not platform().startswith('Windows'):
	    img_files.extend(glob(files_path + '*.jpg'))
	    img_files.extend(glob(files_path + '*.jpeg'))


	flawed_data = 0
	for txt_file in txt_files:
		f = open(txt_file, encoding="utf8")
		line = f.readline()
		data = line.split()
		if len(data) is not 12 or not CheckIfNumeric(data):
			flawed_data += 1
			print('there is a problem with the data in text file: ' 
				+ os.path.basename(txt_file))
			f.close()
			continue
		if not os.path.isfile(files_path + data[0]):
			flawed_data += 1
			print('there is no image file -' + data[0] + '- in this directory')
			f.close()
			continue

		#if not os.path.isfile(txt_file):
		#	fcopy(txt_file, folders_path + 'Output/')

		if not os.path.isfile(folders_path+ 'Output/' + data[0]):
			fcopy(files_path + data[0], folders_path + 'Output/')
			fcopy(txt_file, folders_path + 'Output/')

		else:
			extra_num = 0
			old_name = data[0]
			while os.path.isfile(folders_path+ 'Output/' + data[0]):
				img_name_list = data[0].split('.')
				new_img_name = img_name_list[0] + str(extra_num) + '.' + img_name_list[1]
				data[0] = new_img_name
				extra_num +=1 

			new_line = ' '.join(data)
			f.close()
			new_file_name = folders_path + 'Output/'+  data[0].split('.')[0] + '.txt'
			f = open(new_file_name, 'w', encoding="utf8")
			f.write(new_line)
			f.close()
			fcopy(files_path + old_name, folders_path + 'Output/' + data[0])

	result = '\nfound %d corrupt data file(s)'
	if flawed_data == 0:
		result += ', nothing seems wrong.'

	if len(txt_files) > 0:
	    print(result % flawed_data)
	    print('\nFound %d image(s)' %len(img_files))
	else:
	    print('no files found at %s...' % folder)

	extra_files = len(img_files) - len(txt_files)

	if extra_files > 0:
		img_files = [os.path.basename(img.split('.', 1)[0]) for img in img_files]
		txt_files = [os.path.basename(txt.split('.', 1)[0]) for txt in txt_files] 
		
		print('\nfound %d image file(s) without an associated text file: ' % extra_files)
		for img in img_files:
			if img not in txt_files:
				print(img)

	print('\n====================================\n')





# text file to print the pics
printed_images = open('PrintedImages.txt', 'w+')


input('Displaying images, press any key to continue ...')
print('\n\nN to skip to the next image, B to go back to the prev and P to print the image name.')

if swap_delay == None:
	swap_delay = float(input('enter delay between photos: '))

if newHeight == None:
	newHeight = int(input('enter window height: '))

# read all text files in the Output folder
txt_files = glob(folders_path + '/Output/*.txt')

i = 0
while i < len(txt_files):
	txt = txt_files[i]
	line = open(txt, encoding='utf8').readline().split()

	img_path = folders_path + '/Output/' + line[0]
	img = cv2.imread(img_path)

	img = img.copy()

	x, y, w, h = [int(word) for word in line[1:5]]
	cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 8, cv2.LINE_AA)
	x, y, w, h = [int(word) for word in line[5:9]]
	cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 8, cv2.LINE_AA)
	
	#resize image to fit screen
	newWidth = int(img.shape[1]*newHeight/img.shape[0])
	img = cv2.resize(img, (newWidth, newHeight))

	cv2.imshow("Image Boxes", img)
	
	start_time = time.time()
	
	# record key press
	key = None
	while True:
		key = cv2.waitKey(1)
		end_time = time.time()
		secs = end_time - start_time
		if key == ord('q') or key == ord('n') or secs >=swap_delay:
			i += 1
			break
		elif key == ord('b'):
			i -= 1
			break
		elif key == ord('p') and line[0] not in printed_images:
			# if the image name is not in the file write it again
			printed_images.write(line[0])
			print(line[0])
			break

		pass

	if key == ord('q'):
		break

printed_images.close()
print("End of photos.")
# close image show window
cv2.destroyAllWindows()
