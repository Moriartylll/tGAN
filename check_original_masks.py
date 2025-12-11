import cv2
import numpy as np
import os
import glob

# Check original source masks
original_mask_dir = "tGAN_datasets/New_data/REF_masks101_110/Pos101/PreprocessedPhaseMasks/"
original_masks = sorted(glob.glob(os.path.join(original_mask_dir, "MASK_img_*.tif")))

print(f"Checking {len(original_masks)} masks in source directory: {original_mask_dir}")

count_empty = 0
count_valid = 0

for i, mask_path in enumerate(original_masks[:10]): # Check first 10
    mask = cv2.imread(mask_path, -1) # Use unchanged to be safe
    if mask is None:
        print(f"Failed to read: {mask_path}")
        continue
    
    unique_vals = np.unique(mask)
    if len(unique_vals) == 1 and unique_vals[0] == 0:
        print(f"  [EMPTY] {os.path.basename(mask_path)} - Min: {mask.min()}, Max: {mask.max()}")
        count_empty += 1
    else:
        print(f"  [VALID] {os.path.basename(mask_path)} - Min: {mask.min()}, Max: {mask.max()}, Unique: {unique_vals}")
        count_valid += 1

print(f"\nChecked first 10 files.")

# Also check one mask from our new dataset with -1 flag just in case
new_dataset_mask = "my_new_dataset/train/seg_maps/seq0000/img_000000110.tif"
print(f"\nRe-checking dataset mask {new_dataset_mask} with IMREAD_UNCHANGED...")
mask_new = cv2.imread(new_dataset_mask, -1)
if mask_new is not None:
     print(f"  Min: {mask_new.min()}, Max: {mask_new.max()}, Unique: {np.unique(mask_new)}")
