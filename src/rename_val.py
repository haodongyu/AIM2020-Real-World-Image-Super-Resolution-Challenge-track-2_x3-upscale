import os

input_dir = '../experiment/enhanced_test'

print('Load images from: ', input_dir)

for root, dirs, files in os.walk(input_dir):
    for name in files:
        if name[-3:] == 'png':
            in_path = os.path.join(root, name)
            new_name = in_path[:-4] + '_LR.png'
            os.rename(in_path, new_name)

print('already rename the name to the AIM2020-RealSR official standard')
