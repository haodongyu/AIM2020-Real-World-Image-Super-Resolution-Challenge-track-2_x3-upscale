CUDA_VISIBLE_DEVICES=7 python main.py --model DDet --n_resblocks 32 --n_feats 128 --res_scale 1.0 --data_test Demo --dir_demo /data/yuhaodong/AIM/results-AIM_test_X3_DownSample --scale 3 --save AIM_DDet_finetune_X3_test_model_firtime --test_only --save_results --pre_train ../experiment/model_latest_firtime.pt --n_GPUs 1 --chop