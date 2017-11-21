import cv2, time
from glob2 import glob
from platform import platform

# delay for swapping between pics automatically
swap_delay = None

# hight of the image window
newHeight = None

# speed-up opencv using multithreads
cv2.setUseOptimized(True);
cv2.setNumThreads(8);


if swap_delay == None:
	swap_delay = float(input('enter delay between photos: '))

if newHeight == None:
	newHeight = int(input('enter window height: '))

# read all text files in the Output folder
txt_files = glob('*.txt')

i = 0
while i < len(txt_files):
	txt = txt_files[i]
	line = open(txt, encoding='utf8').readline().split()

	img_path = line[0]
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
		#elif key == ord('p') and line[0] not in printed_images:
		#	# if the image name is not in the file write it again
		#	printed_images.write(line[0])
		#	print(line[0])
		#	break

		

	if key == ord('q'):
		break

printed_images.close()
print("End of photos.")
# close image show window
cv2.destroyAllWindows()
