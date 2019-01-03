import picture
import numpy as np
import sys
import os
from PIL import Image
import cv2
import dehaze

#main variables to change to separate file later on
root_dir = "."
data_dir = os.path.join(root_dir,'data')



def main(debug_mode=0):
    list = os.listdir(data_dir)
    for f in list:
        dehaze.dehaze(f)
        break



def make_haze(img ,coefficient = 0):
    tmp_img = cv2.imread(os.path.join(data_dir,img),-1)
    np_img = np.array(tmp_img)
    t = 0.99
    test_img = np.multiply(np_img,t) #+ A*(1-t)
    print(np_img.shape)
    #show picture
    #picture.show_opened_image(img)
    tmp_test = Image.fromarray(test_img,"RGB")
    tmp_test.show()



if __name__ == '__main__':

    main()

#RESIZE EXAMPLE
#f = cv2.imread(os.path.join(data_dir,f),-1)
#f = cv2.resize(f, (720,480), interpolation = cv2.INTER_CUBIC)
#cv2.imwrite("new.jpg",f)
