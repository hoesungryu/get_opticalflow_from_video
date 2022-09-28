# -------------------
# import package
# -------------------
import os 
import cv2  
import argparse
import numpy as np
from tqdm import tqdm
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

#------------------------------
# user-defined function
#------------------------------
from utils import *


def main(args):
    #------------------------------
    # Arguments
    #------------------------------
    today = args.today
    source_path = args.source_path
    target_path = args.target_path
    target_video_size = args.target_video_size
    os.makedirs(target_path, exist_ok = True ) # make dirs 


    save2npy(file_dir=source_path, 
             save_dir=target_path,
             target_video_size = target_video_size)
    print('[INFO] All video have been converted ... ')




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--today", default=datetime.now().strftime("%Y%m%d_%H%M%S"), type=str)
    parser.add_argument("--target_video_size", default=(256,256), type=tuple, help="convert video size (height, width)")
    parser.add_argument("--source_path",type=str ,default='./video_data')
    parser.add_argument("--target_path",type=str ,default='./video_data_uv')
    args = parser.parse_args()
    print(args.today)
    print("\n".join(f"[INFO] Args: {k}={v}" for k, v in vars(args).items()))
    main(args)