import cv2  
import numpy as np
import matplotlib.pyplot as plt
import os 
from tqdm import tqdm


def save2npy(file_dir, save_dir,target_video_size):
    """Transfer all the videos and save them into specified directory
    Args:
        file_dir: source folder of target videos
        save_dir: destination folder of output .npy files
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    height, width = target_video_size
    
    # List the files
    videos = os.listdir(file_dir)
    videos = [x for x in videos if x.endswith('.mp4')]
    
    for video_name in tqdm(videos):
        # Get src 
        video_path = os.path.join(file_dir, video_name)
        # Get dest 
        save_path = os.path.join(save_dir, video_name[:-4]+'.npy') 
            
        # Load and preprocess video
        data = video2npy(file_path=video_path, resize=(height,width))
        data = np.uint8(data)
        
        # Save as .npy file
        np.save(save_path, data)
    
    return None
def video2npy(file_path, resize):
    """Load video and tansfer it into .npy format
    Args:
        file_path: the path of video file
        resize: the target resolution of output video
    Returns:
        frames: gray-scale video
        flows: magnitude video of optical flows 
    """
    height, width = resize
    # Load video
    cap = cv2.VideoCapture(file_path)
    # Get number of frames
    len_frames = int(cap.get(7))
    # Extract frames from video
    try:
        frames = []
        for i in range(len_frames-1):
            _, frame = cap.read()
            frame = cv2.resize(frame,resize, interpolation=cv2.INTER_AREA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.reshape(frame, (height,width,3))
            frames.append(frame)   
    except:
        print("Error: ", file_path, len_frames,i)
    finally:
        frames = np.array(frames)
        cap.release()
            
    # Get the optical flow of video
    flows = get_opticalflow(frames, resize)
    
#     result = np.zeros((len(flows),height,width,5))
#     result[...,:3] = frames
#     result[...,3:] = flows
    result = np.zeros((len(flows),height,width,2))
    result[...,:2] = flows
    return result
def get_opticalflow(video, resize):
    """Calculate dense optical flow of input video
    Args:
        video: the input video with shape of [frames,height,width,channel]. dtype=np.array
    Returns:
        flows_x: the optical flow at x-axis, with the shape of [frames,height,width,channel]
        flows_y: the optical flow at y-axis, with the shape of [frames,height,width,channel]
    """
    height, width = resize
    
    # initialize the list of optical flows
    gray_video = []
    for i in range(len(video)):
        img = cv2.cvtColor(video[i], cv2.COLOR_RGB2GRAY)
        gray_video.append(np.reshape(img,(height,width,1)))

    flows = []
    for i in range(0,len(video)-1):
        # calculate optical flow between each pair of frames
        flow = cv2.calcOpticalFlowFarneback(gray_video[i], gray_video[i+1], None, 0.5, 3, 15, 3, 5, 1.2, cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
        # subtract the mean in order to eliminate the movement of camera
        flow[..., 0] -= np.mean(flow[..., 0])
        flow[..., 1] -= np.mean(flow[..., 1])
        # normalize each component in optical flow
        flow[..., 0] = cv2.normalize(flow[..., 0],None,0,255,cv2.NORM_MINMAX)
        flow[..., 1] = cv2.normalize(flow[..., 1],None,0,255,cv2.NORM_MINMAX)
        # Add into list 
        flows.append(flow)
        
    # Padding the last frame as empty array
    flows.append(np.zeros((height,width,2)))
      
    return np.array(flows, dtype=np.float32)