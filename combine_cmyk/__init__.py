from PIL import Image, ImageOps
import tifffile
import numpy as np
import tkinter as tk
from tkinter import filedialog
import sys

Image.MAX_IMAGE_PIXELS = None

channel_order = ["Cyan", "Magenta", "Yellow", "Black"]

def get_channel_key(path):
    name = path.lower()
    for i, ch in enumerate(channel_order):
        if ch.lower() in name:
            return i
    print(f"⚠️ Could not detect channel for: {path}")
    sys.exit(1)

root = tk.Tk()
root.withdraw()

file_paths = filedialog.askopenfilenames(
    title="Select the 4 CMYK TIFF files (any order)",
    filetypes=[("TIFF files", "*.tif *.tiff")]
)

if len(file_paths) != 4:
    print("❌ You must select exactly 4 TIFF files!")
    sys.exit(1)

sorted_paths = sorted(file_paths, key=get_channel_key)

# Detect DPI from the first image
first_img = Image.open(sorted_paths[0])
dpi = first_img.info.get("dpi", (72, 72))  # default 72 DPI if missing
first_img.close()

# tifffile expects resolution=(x, y) and resolutionunit=2 (inch)
# Convert DPI to plain floats for tifffile
resolution = (float(dpi[0]), float(dpi[1]))
resolution_unit = 2  # 2 = inch


# Open, invert, convert each channel to 8-bit
channels = [ImageOps.invert(Image.open(path).convert("L")) for path in sorted_paths]
channels_np = [np.array(ch, dtype=np.uint8) for ch in channels]

# Stack as H x W x 4 (C,M,Y,K)
cmyk_array = np.stack(channels_np, axis=-1)

save_path = filedialog.asksaveasfilename(
    defaultextension=".tif",
    filetypes=[("TIFF files", "*.tif *.tiff")],
    title="Save combined CMYK TIFF as"
)

if save_path:
    tifffile.imwrite(
        save_path,
        cmyk_array,
        photometric='separated',
        planarconfig='contig',
        compression='none',
        bigtiff=True,
        resolution=resolution,
        resolutionunit=resolution_unit
    )
    print(f"✅ Saved successfully at {save_path} with DPI={dpi}")
else:
    print("❌ Save canceled.")
