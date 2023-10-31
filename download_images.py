"""
This script will download all images of the Impressions dataset,
to the designated location specified by DEST_DIR.  
"""

import os
import requests
from PIL import Image
import pandas as pd
import io
from tqdm import tqdm


DATA_PATH = "metadata/mean_impact_scores.csv"
DEST_DIR = "media"
root_path = "https://multimodal-impact.s3.amazonaws.com/final_media/"

if not os.path.exists(DEST_DIR):
    os.mkdir(DEST_DIR)

# loading dataset with all ImgIds:
data = pd.read_csv(DATA_PATH)
if "Unnamed: 0" in data.columns:
    data = data.drop(columns=["Unnamed: 0"])
    data.to_csv(DATA_PATH, index=False)

# downloading all images:
for imgid in tqdm(list(data.ImgId), total=len(data)):
    url = os.path.join(root_path, imgid + ".png")
    img_data = requests.get(url).content
    img = Image.open(io.BytesIO(img_data))
    img_path = os.path.join(DEST_DIR, imgid + ".png")
    img.save(img_path)

print(f"\nDownload complete. All images saved to {DEST_DIR}.\n")
