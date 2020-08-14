import os
import shutil
from PIL import Image
from PIL import ImageOps
import PIL
import numpy as np

import pickle

input_image_dir = '../experiment/AIM_WDDet_x3_TEST_model_best_forensemble/results-Demo'
cropping_image_dir = '../experiment/AIM_WDDet_x3_TEST_model_best_forensemble/results-Demo'

with open('./padding_dict.pkl', 'rb') as f:
    padding_dict = pickle.load(f)


for root, dirs, files in os.walk(input_image_dir):
    for name in files:
        if name[-3:] == 'png':
            print('Processing : ', name)
            in_path = os.path.join(root, name)
            img = Image.open(in_path)
            right = padding_dict[name.replace('_LR', '')][0]
            bottom = padding_dict[name.replace('_LR', '')][1]
            print(img.size)
            img = ImageOps.crop(img, (0, 0, right, bottom))
            print(img.size)
            print('======================')
            out_path = os.path.join(cropping_image_dir, name)
            img.save(out_path)
