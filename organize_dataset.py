import os
import shutil
import glob

# Configuration
source_base = "tGAN_datasets/New_data"
dest_base = "my_new_dataset"

raw_data_dir = os.path.join(source_base, "REF_raw_data101_110")
mask_data_dir = os.path.join(source_base, "REF_masks101_110")

train_sequences = [f"Pos{i}" for i in range(101, 109)] # 101 to 108
test_sequences = [f"Pos{i}" for i in range(109, 111)] # 109 to 110

def prepare_dataset(sequences, split_name):
    print(f"Processing {split_name} set...")
    
    dest_img_base = os.path.join(dest_base, split_name, "images")
    dest_mask_base = os.path.join(dest_base, split_name, "seg_maps")
    
    os.makedirs(dest_img_base, exist_ok=True)
    os.makedirs(dest_mask_base, exist_ok=True)
    
    for idx, pos_name in enumerate(sequences):
        seq_name = f"seq{idx:04d}" # seq0000, seq0001...
        print(f"  Processing {pos_name} -> {seq_name}")
        
        src_img_dir = os.path.join(raw_data_dir, pos_name, "aphase")
        src_mask_dir = os.path.join(mask_data_dir, pos_name, "PreprocessedPhaseMasks")
        
        dst_img_dir = os.path.join(dest_img_base, seq_name)
        dst_mask_dir = os.path.join(dest_mask_base, seq_name)
        
        os.makedirs(dst_img_dir, exist_ok=True)
        os.makedirs(dst_mask_dir, exist_ok=True)
        
        # Process Images
        # Filter for .tiff and ignore .Zone files implicitly by glob pattern if possible, or manual filter
        image_files = sorted(glob.glob(os.path.join(src_img_dir, "img_*.tiff")))
        
        for img_path in image_files:
            filename = os.path.basename(img_path)
            if "Zone.Identifier" in filename:
                continue
            
            # Copy image
            shutil.copy2(img_path, os.path.join(dst_img_dir, filename))
            
            # Find corresponding mask
            # Image: img_000000000.tiff
            # Mask: MASK_img_000000000.tif
            
            mask_filename = "MASK_" + filename.replace(".tiff", ".tif")
            mask_path = os.path.join(src_mask_dir, mask_filename)
            
            if os.path.exists(mask_path):
                # Copy and rename mask to match image filename (but keep extension or make consistent? 
                # Let's make it consistent: img_000000000.tif)
                new_mask_filename = filename.replace(".tiff", ".tif") # img_000000000.tif
                shutil.copy2(mask_path, os.path.join(dst_mask_dir, new_mask_filename))
            else:
                print(f"    Warning: Mask not found for {filename}")

if __name__ == "__main__":
    if os.path.exists(dest_base):
        print(f"Removing existing {dest_base}...")
        shutil.rmtree(dest_base)
        
    prepare_dataset(train_sequences, "train")
    prepare_dataset(test_sequences, "test")
    print("Done!")
