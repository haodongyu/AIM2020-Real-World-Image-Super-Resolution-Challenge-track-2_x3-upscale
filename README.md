# AIM2020-Real-World-Image-Super-Resolution-Challenge-track-2_x3-upscale  
# Real Image Super-Resolution Track 2 Upscaling x3

## 1. Quick Start

If now you are in the folder "AIM2020-RealSR-x3-AiAiR", you can run

```sh
cd ./src
sh reproduce_testset_results.sh
```

## 2. Where is the test_data
`./test_data/TestLRX3/TestLR/`
The testing dataste has been included in zip file.


## 3. where is the outputs ?
`./experiment/enhanced_test` which should be the same as our uploaded SR images.


## 4. enviriment needed
```
python>=3.6
Pytorch>=1.4
numpy
skimage
imageio
matplotlib
tqdm
cv2
```
We conduct all experiments on 8 TITAN RTX GPUs.

## 5. code structure
```
--root
  |
  |--test_data: test images
  |--experiment: dir for the obtained model and results

  |--src: all the codes for the network

​        |data--: self defined dataloader for the network

​        |loss--: loss function 

​        |model--: DDet, WDDet, EDSR and other network 


--README.md: this file
```
