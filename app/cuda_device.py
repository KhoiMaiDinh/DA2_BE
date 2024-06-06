import torch
import numpy as np
import random

class Device():

    def __init__(self):
        super(Device, self).__init__()
        seed=1
        random.seed(seed)   
        torch.manual_seed(seed)
        np.random.seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

        self.device = torch.device('cpu')
        

    # def getDevice():
    #     return self.device