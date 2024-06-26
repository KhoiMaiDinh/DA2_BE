import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from PIL import Image
import sys
import random
import shutil
from .model import Detector
import argparse
from datetime import datetime
from tqdm import tqdm
from retinaface.pre_trained_models import get_model
from .preprocess import extract_face
import warnings
import cv2
warnings.filterwarnings('ignore')
from ...cuda_device import Device

def main(img):
    cuda_device = Device()
    device = cuda_device.device
    model=Detector()
    model=model.to(device)
    cnn_sd=torch.load("app/weights/FFraw.tar", map_location='cpu')["model"]
    model.load_state_dict(cnn_sd)
    model.eval()

    frame = img
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_detector = get_model("resnet50_2020-07-20", max_size=max(frame.shape),device=device)
    face_detector.eval()

    face_list=extract_face(frame,face_detector)

    with torch.no_grad():
        if len(face_list) > 0:
            img=torch.tensor(face_list).to(device).float()/255
        else:
            image_size=(380,380)
            frame = cv2.resize( frame,dsize=image_size).transpose((2,0,1))
            frames =[frame]
            img=torch.tensor(frames).to(device).float()/255
        # torchvision.utils.save_image(img, f'test.png', nrow=8, normalize=False, range=(0, 1))
        pred=model(img).softmax(1)[:,1].cpu().data.numpy().tolist()

    print(f'fakeness: {max(pred):.4f}')
    return max(pred)



