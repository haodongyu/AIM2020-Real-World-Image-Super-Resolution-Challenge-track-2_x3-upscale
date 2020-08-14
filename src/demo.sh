#CUDA_VISIBLE_DEVICES=0,1,3,5 python main.py --n_GPUs 4 --model DDet --scale 3 --save AIM_DDet_X3_new50epoch --n_resblocks 32 --n_feats 128 --res_scale 1.0 --data_train AIM --data_test AIM --batch_size 24 --reset --patch_size 144 --n_threads 4 --split_batch 1 --lr 5e-6 --epochs 50 --loss 1.0*L1 --pre_train ../experiment/AIM_DDDet_x3/model/model_latest.pt --chop

#CUDA_VISIBLE_DEVICES=1,3,5,7 python main.py --model DDet --scale 3 --save DIV2K_DDDet_x3_new50epoch --n_resblocks 32 --n_feats 128 --res_scale 1.0 --data_train DIV2K --data_test DIV2K --batch_size 32 --dir_data /data/zhoubo/dataset --n_GPUs 4 --reset --patch_size 144 --n_threads 4 --split_batch 1 --lr 1e-6 --epochs 50 --loss 1.0*L1 --pre_train ../experiment/A --chop
CUDA_VISIBLE_DEVICES=0,1,3,5 python main.py --model DDet --scale 3 --save AIM_DDDet_x3_finetune_afternew50 --n_resblocks 32 --n_feats 128 --res_scale 1.0 --data_train AIM --data_test AIM --batch_size 4 --dir_data /data/yuhaodong --n_GPUs 4 --reset --patch_size 402 --n_threads 4 --split_batch 1 --lr 5e-5 --decay 120-240-360 --epochs 480 --loss 20.0*SSIM --pre_train ../experiment/AIM_DDet_X3_new50epoch/model/model_latest.pt --save_models --chop

#--deep-supervision True 
# --loss 1.0*MSE
# --loss 1.0*L1+10.0*SSIM
# --patch_size 256
# --ext bin