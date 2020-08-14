import os
import shutil
from PIL import Image
from PIL import ImageOps
import PIL
import numpy as np

import pickle

input_image_dir = '../test_data/TestLRX3/TestLR/'
padding_image_dir = '../test_data/TestLRX3/TestLR_padding'
cropping_image_dir = './TestLR_cropping'

if os.path.exists(padding_image_dir):
    shutil.rmtree(padding_image_dir)
os.mkdir(padding_image_dir)

padding_dict = {}

for root, dirs, files in os.walk(input_image_dir):
    for name in files:
        if name[-3:] == 'png':
            print('Processing : ', name)
            in_path = os.path.join(root, name)
            img = Image.open(in_path)
            right = img.size[0]%2
            bottom = img.size[1]%2
            print(img.size)
            img = ImageOps.expand(img, (0, 0, right, bottom), 0)
            print(img.size)
            print('======================')
            out_path = os.path.join(padding_image_dir, name)
            img.save(out_path)
            padding_dict[name.replace('_LR','')] = (right*3, bottom*3)

with open('./padding_dict.pkl', 'wb') as f:
    pickle.dump(padding_dict, f)
