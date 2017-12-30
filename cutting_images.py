
# coding: utf-8

# ## Importing necessary libraries

# In[1]:

#imports
import glob2
#numpy and matplotlib
import numpy as np # for reading images and handling matrix operations
import matplotlib.pyplot as plt #plotting lib
import matplotlib
from PIL import Image
from numpy import *
import pandas as pd #


# ## Reading needed data from disk

# In[2]:

#reading the text files and images
txt_data = [] #list to hold all the text data
img_data = [] #list to hold all images

#the path to the txt data files
file_path = 'Neural_Data/' 
glob_files = glob2.glob(file_path + '*.txt')

#open all the txt files
for file in glob_files:
     with open(file) as f:
        text = f.readline()
        #print(text)
        txt_data.append(text) #store text data in a list
        img_name = text.split()[0] #get the name of the image
        im = Image.open(file_path + img_name) #open the image
        img_data.append(im) #store the image data in a list
        
#show first 5 images
IMG_SIZE= (12, 8) 
for i in range(0, 5):
    plt.figure(figsize=IMG_SIZE)
    plt.imshow(img_data[i])
    print(txt_data[i])
    
plt.show()


# ## Cleaning the data and preparing it for the CNN

# In[3]:

#splitting the text data and putting it into a pandas data frame for easy reading
txt_df = pd.DataFrame({'ImageName': [img_name.split()[0] for img_name in txt_data],
                       'Car_X' : [int(car_x.split()[1]) for car_x in txt_data],
                       'Car_Y' : [int(car_y.split()[2]) for car_y in txt_data],
                       'Car_Width' : [int(car_width.split()[3]) for car_width in txt_data],
                       'Car_Height' : [int(car_height.split()[4]) for car_height in txt_data],
                       'NumPlate_X' : [int(numplate_x.split()[5]) for numplate_x in txt_data],
                       'NumPlate_Y' : [int(numplate_y.split()[6]) for numplate_y in txt_data],
                       'NumPlate_Width' : [int(numplate_width.split()[7]) for numplate_width in txt_data],
                       'NumPlate_Height' : [int(numplate_height.split()[8]) for numplate_height in txt_data],
                       'CarColor' : [car_color.split()[9] for car_color in txt_data],
                       'CarType' : [car_type.split()[10] for car_type in txt_data],
                       'NumPlateNumber' : [numplate_num.split()[11].replace('_', ' ') for numplate_num in txt_data] # show the number plate with spaces here
                      })

# re-arrange the pandas dataframe to be in the correct order
txt_df = txt_df[['ImageName', 'Car_X', 'Car_Y', 'Car_Width', 'Car_Height', 'NumPlate_X', 'NumPlate_Y','NumPlate_Width', 'NumPlate_Height',
                 'CarColor', 'CarType', 'NumPlateNumber']]

#show the first 10 entries
txt_df.head(10)


# In[4]:

car_imgs = []
numplate_imgs = []

for i in range(0, len(img_data)):
    img = np.array(img_data[i])
    car_x = txt_df['Car_X'][i]
    car_y = txt_df['Car_Y'][i]
    car_width = txt_df['Car_Width'][i] + car_x
    car_height = txt_df['Car_Height'][i] + car_y
    numplate_x = txt_df['NumPlate_X'][i]
    numplate_y = txt_df['NumPlate_Y'][i]
    numplate_width = txt_df['NumPlate_Width'][i] + numplate_x
    numplate_height = txt_df['NumPlate_Height'][i] + numplate_y
    car_img = img[car_y:car_height, car_x:car_width]
    numplate_img = img[numplate_y:numplate_height, numplate_x:numplate_width]
    car_imgs.append(car_img)
    numplate_imgs.append(numplate_img)

#show the first 3 images
IMG_SIZE= (6, 4)  
for i in range(0, 3):
    plt.figure(figsize=IMG_SIZE)
    plt.imshow(car_imgs[i])
    plt.figure(figsize=IMG_SIZE)
    plt.imshow(numplate_imgs[i])

plt.show()


# In[5]:

def resize_image(numpy_array_image, new_height, new_width):
    # convert nympy array image to PIL.Image
    image = Image.fromarray(numpy_array_image)
    #old_width = float(image.size[0])
    #old_height = float(image.size[1])
    #ratio = float( new_height / old_height)
    #new_width = int(old_width * ratio)
    image = image.resize((new_width, new_height), Image.NEAREST)# PIL.Image.ANTIALIAS)
    # convert PIL.Image into nympy array back again
    return array(image)


# In[6]:

# input image dimensions
img_rows, img_cols = 200, 200

# number of channels
img_channels = 3

master_car_data= []
car_labels = []
#data
for im in car_imgs: 
    #img = np.resize(im, (img_rows,img_cols))#, Image.NEAREST)
    img = resize_image(im, img_rows, img_cols)
    #data = np.asarray( img, dtype='uint8')
    master_car_data.append(img)
    car_labels.append(1)

car_labels = np.asarray(car_labels)

