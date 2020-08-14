import os
import shutil
from PIL import Image
import PIL
import numpy as np
from config import *

weights_norm = 0.
for key in weights.keys():
    weights_norm += weights[key]
weights_norm /= float(len(weights.keys()))

target_dir = '../experiment/enhanced_test'
img_pool = {}

for input_dir in dir_pools:
    try:
        for root, dirs, files in os.walk(input_dir):
            for name in files:
                if name[-3:] == 'png':
                    print('Processing : ' + name)
                    in_path = os.path.join(root, name)
                    img = Image.open(in_path)
                    if name not in img_pool.keys():
                        img_pool[name] = np.array(img, dtype=np.float32) * weights[input_dir] / weights_norm
                    else:
                        img_pool[name] += np.array(img, dtype=np.float32) * weights[input_dir] / weights_norm
    except Exception as e:
        print(e.args)
        print(str(e))
        print(repr(e))
        pass

for key in img_pool.keys():
    try:
        img = Image.fromarray(np.array(np.round(np.clip(img_pool[key]/float(len(dir_pools)), 0., 255.)), dtype='uint8'))
        out_path = os.path.join(target_dir, key)
        img.save(out_path)
        print('Generating : ' + out_path)
    except Exception as e:
        print(e.args)
        print(str(e))
        print(repr(e))
        pass

for input_dir in dir_pools:
    try:
        os.rmdir(input_dir)
    except Exception as e:
        print(e.args)
        print(str(e))
        print(repr(e))
        pass
