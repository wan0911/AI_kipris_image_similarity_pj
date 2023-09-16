import os
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np
import pytorch_lightning as pl
import torchvision
from PIL import Image
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize

from lightly.data import LightlyDataset, collate
from lightly.loss import NTXentLoss
from lightly.models.modules.heads import SimCLRProjectionHead

from pathlib import Path
import shutil
from pymongo import MongoClient
import re
import pickle

# mongo
MONGO_URI = ""
MONGO_DB = "markData"
MONGO_COLLECTION = "mark_data"

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# model_path
BASE_DIR = Path.cwd() / "app"  # app
STATIC_DIR = os.path.join(BASE_DIR, "static/img")
INPUT_DIR = os.path.join(STATIC_DIR, "input")
FM_DIR = os.path.join(STATIC_DIR, "fm_img")
FM_INPUT_DIR = os.path.join(FM_DIR, "fm_input")

MODEL_DIR = os.path.join(BASE_DIR, "models/simCLR")
DATA_DIR = Path(__file__).resolve().parent / "data-100k"
CKPT_DIR = Path(__file__).resolve().parent / "trained_weights.ckpt"
EMBED_DIR = os.path.join(MODEL_DIR, "embeddings.pkl")
FILENAME_DIR = os.path.join(MODEL_DIR, "filenames.pkl")
seed = 1
input_size = 128
pl.seed_everything(seed)


# 비공개
## 참고 논문 = 

