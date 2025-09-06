# Combine four single-channel TIFFs (C, M, Y, K) into one untagged CMYK TIFF — perfect for print/RIP workflows that export separations as individual files.

✅ Saves as true CMYK (Photometric=Separated, not RGB or Gray)
✅ 8-bit channels
✅ Untagged CMYK (no embedded ICC profile)
✅ BigTIFF enabled (handles very large images)
✅ No compression by default (lossless, safest for print)
✅ Keeps DPI from the first channel when available (falls back to 72 DPI)
✅ Simple file picker — no command-line arguments needed
✅ Auto-detects channel order from filenames

## What this is for

Many RIPs or prepress tools output four separate grayscale TIFFs, one per separation: Cyan, Magenta, Yellow, Black. Some downstream tools, though, expect a single CMYK file with all four channels packed together.
This tool takes those four files and produces one 8-bit, untagged CMYK BigTIFF.

## File naming rules (important)

For channel detection, filenames must end with these case-insensitive suffixes:
…Cyan.tif
…Magenta.tif
…Yellow.tif
…Black.tif

Examples (good):

job123_Cyan.tif
job123_Magenta.tif
job123_Yellow.tif
job123_Black.tif


Examples (bad – won’t be recognized):

C.tif             # too short / ambiguous
job123_C.tif      # not the required suffix
job123_cy.tif     # not "Cyan"
job123_black1.tif # anything after Black breaks the match


Tip: Keep the base name identical and only change the trailing channel word.

# Install

## Option A — install directly from your Git repo

````
pip install "git+https://github.com/bloodsugar420/combine-cmyk.git@v0.0.5"
````
Option B — install locally (no GitHub)

From the project folder (where pyproject.toml lives):

pip install .

Dependencies (Pillow, tifffile, numpy) are installed automatically.

Requires Python 3.8+.

Use

Run the tool:

If installed:

python -m combine_cmyk


Or double-click combine_cmyk.py if you’re working from the raw script.

In the file picker, select the four TIFFs (any order).
The tool will detect the channel by your filename suffix (see naming rules above).

The tool inverts each channel (because separations are typically exported inverted).

Pick a save location for the combined CMYK TIFF.

That’s it. You’ll get a single untagged CMYK BigTIFF, 8-bit, with no compression and DPI copied from the first channel if present (or 72 DPI if missing).

What it writes (technical details)

Photometric: Separated (CMYK)
Planar configuration: Contig (interleaved C, M, Y, K)
Bit depth: 8-bit per channel
Compression: none
ICC profile: none (untagged CMYK)
BigTIFF: enabled
Resolution: copied from first input (if present), otherwise 72×72 DPI

Troubleshooting

“Repository not found” when installing
Make sure you replaced <YOURUSERNAME> with your actual GitHub username and that you pushed the repo and the tag.

Photoshop shows ‘Untagged Gray’ instead of CMYK
This tool writes Photometric=Separated with PlanarConfig=Contig, so it should appear as CMYK. If you see Gray, confirm you’re running the latest version and that your downstream app supports CMYK BigTIFF.

Wrong channels / swapped colors
Check filenames end exactly with the required suffixes (…Cyan.tif, …Magenta.tif, …Yellow.tif, …Black.tif). The tool maps channels strictly from those suffixes.

DPI isn’t what I expect
DPI is copied from the first selected file if present; otherwise it defaults to 72. Ensure the first file has the correct DPI metadata if you rely on it.

Huge files fail with classic TIFF limits
This tool writes BigTIFF, which supports files > 4 GB. If you still hit issues, ensure you have enough RAM/disk and try saving to a local SSD.

I need compression
Set the writer to compression='lzw' (lossless). Default is none for maximum fidelity/compatibility.

Roadmap / custom tweaks

Optional: disable inversion if your inputs are already positive.

Optional: progress bar on save for very large outputs.

Optional: CLI flags for headless operation (keep GUI by default).

License

Choose a license you prefer (e.g., MIT). Add LICENSE to the repo.

Credits

Built with ❤️ using Pillow, tifffile, and NumPy.
