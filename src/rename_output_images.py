import os
import shutil
from config import *

for input_dir in dir_pools:
    try:
        for root, dirs, files in os.walk(input_dir):
            for name in files:
                if name[-3:] == 'png':
                    in_path = os.path.join(root, name)
                    tar_path = input_dir + '/' + name
                    shutil.move(in_path, tar_path)
                    new_path = tar_path.replace('_LR', '')
                    os.rename(tar_path, new_path)

        os.remove(input_dir + '/config.txt')
        os.remove(input_dir + '/log.txt')
        os.rmdir(input_dir + '/model')
        os.rmdir(input_dir + '/results-Demo')
    except Exception as e:
        print(e.args)
        print(str(e))
        print(repr(e))
        pass