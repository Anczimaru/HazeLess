import cv2
import os
import sys
from PIL import Image
import numpy as np
import picture
import math

root_dir = "."
data_dir = os.path.join(root_dir,'data')

def dehaze(f):
    dark_channel = get_dark_channel(f)
    A = get_atmosphere_coeff(f,dark_channel)
    return 0



def get_dark_channel(f,pad_size=5):
    tmp_img = cv2.imread(os.path.join(data_dir,f),-1)
    padded_img = cv2.copyMakeBorder(tmp_img,5,5,5,5,cv2.BORDER_REPLICATE)
    picture.show_opened_image(padded_img)
    np_img = np.array(tmp_img)
    (x,y,z) = np_img.shape
    print(np_img.shape)
    bw_img = cv2.cvtColor(padded_img, cv2.COLOR_BGR2GRAY)
    picture.show_opened_image(bw_img)
    dark_channel = np.zeros((x,y))
    for j in range(x):
        for i in range(y):
            patch = bw_img[j:(j+2*pad_size),i:(i+2*pad_size)]
            dark_channel[j,i] = patch.min()


    print(dark_channel.shape)
    tmp_test = Image.fromarray(dark_channel,"L")
    print("Dark channel created")
    return dark_channel



def get_atmosphere_coeff(f, dark_channel, pixel_coeff=0.01):
    tmp_img = cv2.imread(os.path.join(data_dir,f),-1)
    np_img = np.array(tmp_img)
    (x,y,z) = np_img.shape
    n_pixels = x*y
    searched_pixels = math.floor(n_pixels*pixel_coeff)
    dark_vector = np.reshape(dark_channel,(-1,n_pixels))
    image_vector = np.reshape(np_img, (-1,n_pixels,3))
    print(dark_vector.shape)
    print(image_vector.shape)
    indexes = np.sort(dark_vector)
    indexes = indexes[::-1]
    indexes = indexes.astype(int)
    print(indexes.shape)
    param = np.zeros((1,3))
    tmp_vec = np.zeros((1,3))
    for k in range(searched_pixels):
        #index = indexes[0,k]
        #tmp_vec = image_vector[:,index]
        param = param+image_vector[:,indexes[0,k]]
    atmospehere = param/searched_pixels
    print(atmospehere)
    return atmospehere


def get_laplacian(f):
    ddepth = cv2.CV_16S
    kernel_size = 3
    tmp_img = cv2.imread(os.path.join(data_dir,f),-1)
    # Remove noise by blurring with a Gaussian filter
    tmp_img = cv2.GaussianBlur(tmp_img, (3, 3), 0)

    tmp_img_gray = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(src_gray, ddepth, kernel_size)
    return laplacian
