# -------------------
# import package
# -------------------
import os 
import cv2  
import argparse
import numpy as np
from tqdm import tqdm
from glob import glob 
from datetime import datetime
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

#------------------------------
# user-defined function
#------------------------------
from utils import *

def save_optic_image(npy_save_path, vis_save_path):
    for npy_file in glob(npy_save_path+'/*.npy'):
        file_name = os.path.basename(npy_file)
        save_folder = os.path.join(vis_save_path,file_name[:-4] )
        os.makedirs(save_folder, exist_ok = True )

        tmp_npy = np.load(npy_file)
        for idx in range(tmp_npy.shape[0]-1):
            save_name = os.path.join(save_folder,file_name[:-4]+f'_{idx:03d}.jpg' )
            
            flow_color = flow_to_color(tmp_npy[idx], convert_to_bgr=False)
            plt.imshow(flow_color, cmap='jet')
            plt.savefig(save_name,bbox_inches='tight',pad_inches=0)
            plt.axis('off')
            plt.close()
    return None

def main(args):
    #------------------------------
    # Arguments
    #------------------------------
    today = args.today
    npy_save_path = args.npy_save_path
    vis_save_path = args.vis_save_path
    os.makedirs(vis_save_path, exist_ok = True ) # make dirs 
    
    save_optic_image(npy_save_path, vis_save_path)
    print('[INFO] All images have been saved ... ')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--today", default=datetime.now().strftime("%Y%m%d_%H%M%S"), type=str)
    parser.add_argument("--vis_save_path",type=str ,default='./video_data_uv_vis')
    parser.add_argument("--npy_save_path",type=str ,default='./video_data_uv')
    args = parser.parse_args()
    print(args.today)
    print("\n".join(f"[INFO] Args: {k}={v}" for k, v in vars(args).items()))
    main(args)