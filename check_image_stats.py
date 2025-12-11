import cv2
import numpy as np
import os
import glob

# Path to one of your training images
img_path = glob.glob("my_new_dataset/train/images/seq0000/*.tiff")[0]
mask_path = glob.glob("my_new_dataset/train/seg_maps/seq0000/*.tif")[0]

print(f"Checking Image: {img_path}")
print(f"Checking Mask: {mask_path}")

# 1. Try Default Reading (as used in current data loader)
img_default = cv2.imread(img_path, 0)
print(f"\n[Default Read - cv2.imread(path, 0)]")
if img_default is None:
    print("Error: Could not read image.")
else:
    print(f"Shape: {img_default.shape}")
    print(f"Dtype: {img_default.dtype}")
    print(f"Min: {img_default.min()}, Max: {img_default.max()}, Mean: {img_default.mean()}")
    if img_default.max() == 0:
        print("ALERT: Image is ALL BLACK (0)!")

# 2. Try Unchanged Reading (better for 16-bit)
img_unchanged = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
print(f"\n[Unchanged Read - cv2.imread(path, -1)]")
if img_unchanged is None:
    print("Error: Could not read image.")
else:
    print(f"Shape: {img_unchanged.shape}")
    print(f"Dtype: {img_unchanged.dtype}")
    print(f"Min: {img_unchanged.min()}, Max: {img_unchanged.max()}, Mean: {img_unchanged.mean()}")

# 3. Check Mask
mask = cv2.imread(mask_path, 0)
print(f"\n[Mask Read]")
if mask is None:
    print("Error: Could not read mask.")
else:
    print(f"Shape: {mask.shape}")
    print(f"Dtype: {mask.dtype}")
    print(f"Min: {mask.min()}, Max: {mask.max()}, Unique Values: {np.unique(mask)}")
