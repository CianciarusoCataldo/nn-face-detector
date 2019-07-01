import os
import subprocess
import logging

import numpy as np
np.random.seed(123)

import torch
torch.manual_seed(123)
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from PIL import Image
import cv2
from age_detection.utils.img_to_vec import Img2Vec

execution_path=os.getcwd()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger("tensorflow").setLevel(logging.ERROR)

class Age_Detector(nn.Module):

    def __init__(self, st=os.path.join(os.path.join(execution_path,"models"),"age_est_model.pt"), input_unit_size=512, hidden_layer1_size=256, hidden_layer2_size=128, output_layer_size=1):
        super(Age_Detector, self).__init__()
        self._imgtovec = Img2Vec(cuda=False)
        self.layer1    = nn.Linear(input_unit_size, hidden_layer1_size)
        nn.init.xavier_uniform(self.layer1.weight)

        self.layer2    = nn.Linear(hidden_layer1_size, hidden_layer2_size)
        nn.init.xavier_uniform(self.layer2.weight)

        self.layer3    = nn.Linear(hidden_layer2_size, output_layer_size)
        nn.init.xavier_uniform(self.layer3.weight)
        self.load_state_dict(torch.load(st))


    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = self.layer3(x)
        return x


    def detect_age(self, s_image):
        im=np.copy(s_image)
        img=Image.fromarray(im)
        img = img.resize((224, 224))
        image_feats = self._imgtovec.get_vec(img).reshape(1, -1)
        res=self(Variable(torch.from_numpy(image_feats).float())).data.cpu().numpy()[0][0]
        return int(res)

if __name__ == '__main__':
    pass
