# run basic models, self-ensemble + crop-ensemble
CUDA_VISIBLE_DEVICES=0,1,2,3 python main.py --model DDet --n_resblocks 32 --n_feats 128 --res_scale 1.0 --data_test Demo --scale 3 --save AIM_DDet_x3_TEST2_model12_forensemble --save_results --reset --test_only --dir_demo ../test_data/TestLRX3/TestLR --pre_train ../experiment/model_DDet_12.pt --n_GPUs 4 --chop --chop-size 450 450 450 450 --shave-size 100 100 10 10
CUDA_VISIBLE_DEVICES=0,1,2,3 python main.py --model DDet --n_resblocks 32 --n_feats 128 --res_scale 1.0 --data_test Demo --scale 3 --save AIM_DDet_x3_TEST2_model18_forensemble --save_results --reset --test_only --dir_demo ../test_data/TestLRX3/TestLR --pre_train ../experiment/model_DDet_18.pt --n_GPUs 4 --chop --chop-size 450 450 450 450 --shave-size 100 100 10 10
CUDA_VISIBLE_DEVICES=0,1,2,3 python main.py --template EDSR_paper --res_scale 1.0 --data_test Demo --scale 3 --save AIM_EDSR_x3_TEST_model_best_forensemble --save_results --reset --test_only --dir_demo ../test_data/TestLRX3/TestLR --pre_train ../experiment/model_edsr_best.pt --n_GPUs 4 --chop --self_ensemble --chop-size 450 --shave-size 100
python image_expanding.py
CUDA_VISIBLE_DEVICES=0,1,2,3 python main.py --model WDDET --n_resblocks 40 --n_feats 128 --res_scale 1.0 --data_test Demo --scale 3 --save AIM_WDDet_x3_TEST_model_best_forensemble --save_results --reset --test_only --dir_demo ../test_data/TestLRX3/TestLR_padding --pre_train ../experiment/model_wddet_best.pt --n_GPUs 4 --chop --chop-size 300 --shave-size 50

# # remove log/config files, rename SR images

python image_cropping.py
python rename_output_images.py

# # model-ensemble
python model_ensemble.py

# # rename the img_names as the input LR image
python rename_val.py