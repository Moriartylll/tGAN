# tGAN

This repository hosts the training and evaluation code for "tGAN: Enhanced Cell Tracking Using A GAN-based Super-Resolution Video-to-Video Time-Lapse Microscopy Generative Model." 

This model is designed to significantly enhance the quality and diversity of synthetic annotated time-lapse microscopy data. Our model features a dual-resolution architecture that adeptly synthesizes both low and high-resolution video frames, uniquely capturing the intricate dynamics of cellular processes essential for accurate tracking. ![Screenshot](Figure1.png)

### Requirements

* Optional: Create a conda or Python virtual environment.

* Install the required packages using:
```
pip install -r requirements.txt
```

### Data Preprocessing for Custom Datasets

To utilize tGAN with your own cell microscopy datasets, you must first organize your data into a specific directory structure. The system expects raw image data and corresponding segmentation masks to be prepared as follows:

**Source Data Example:**
We commonly uses datasets such as `REF_masks101_110`, `REF_raw_data101_110`, `RIF10_masks201_210`, and `RIF10_raw_data201_210`. For this example, we will focus on the `REF` datasets (`REF_masks101_110` and `REF_raw_data101_110`). The raw image data typically resides in a structure like `REF_raw_dataXXX/PosXXX/aphase/`, while the masks are found under `REF_masksXXX/PosXXX/PreprocessedPhaseMasks/` with names like `MASK_img_000000000.tif`.

**Required Target Structure:**
Your processed dataset should adhere to the following layout, distinguishing between training and testing splits:

```
my_new_dataset/
├── train/                  # Used for model training
│   ├── images/             # Real microscopy images (Ground Truth Images)
│   │   ├── seq0000/
│   │   ├── seq0001/
│   │   └── ... 
│   └── seg_maps/           # Corresponding segmentation masks
│       ├── seq0000/
│       ├── seq0001/
│       └── ... 
└── test/                   # Used for model evaluation
    ├── images/             # Real microscopy images (for comparison)
    │   ├── seq0000/
    │   └── seq0001/
    └── seg_maps/           # Input segmentation masks for inference
        ├── seq0000/
        └── seq0001/
```

**Preprocessing Script:**
Use the `organize_dataset.py` script to automatically transform your raw data into the required format. This script handles the sequence splitting (e.g., 80% for training, 20% for testing), directory creation, and renaming of files (e.g., `MASK_img_XXX.tif` to `img_XXX.tif`) to ensure compatibility with our data loaders.

To run the preprocessing for your new dataset (assuming your raw data is in `tGAN_datasets/New_data/`), execute the following command:

```bash
python organize_dataset.py
```
This script will create the `my_new_dataset/` directory with the appropriate `train/` and `test/` subfolders.

### Usage

#### 1. Retraining Models on a New Dataset
If you intend to use tGAN on a new dataset (such as the one prepared in the previous step), you must retrain **both** the low-resolution and super-resolution models.

**Train the Low-Resolution Video-to-Video Model:**
This script trains the model that generates low-resolution frames from segmentation masks.
```bash
python train_low_res_vid2vid.py --train_set_dir my_new_dataset/train/ --lr 0.0001 --p_vanilla 0.2 --p_diff 0.2 --output_dir checkpoints/low_res/
```

**Train the Super-Resolution Image-to-Image Model:**
This script trains the model that upscales the low-resolution frames to high resolution.
```bash
python train_sup_res_img2img.py --train_set_dir my_new_dataset/train/ --lr 0.0001 --p_vanilla 0.2 --p_diff 0.2 --output_dir checkpoints/sup_res/
```

#### 2. Using Trained Models (End-to-End Inference)
Once you have trained the models (or if you have pre-trained weights), you can generate the final enhanced outputs using the `test_end2end.py` script.

This script acts as the pipeline that connects your trained models:
1.  It loads the **Low-Resolution Generator**.
2.  It loads the **Super-Resolution Generator**.
3.  It takes your test set segmentation masks, generates a low-res video, and then enhances it to a high-res video.

**Run the inference:**
```bash
python test_end2end.py --test_set_dir my_new_dataset/test/ --low_res_gen_ckpt_dir checkpoints/low_res/ --sup_res_gen_ckpt_dir checkpoints/sup_res/ --output_dir results/ --n_frames_total 10
```

**Outputs:**
The script will save the generated frames (both low-res and super-res) in the specified `--output_dir` and will output evaluation metrics (FVD, SSIM, PSNR, LPIPS) to the console to assess the quality of the generation.

