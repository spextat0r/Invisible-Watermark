# Invisible-Watermark

Invisible-Watermark is a steganography tool written in python that does not hide text data in an image's pixels but instead hides the text in the image itself.

![Help](/assets/images/Help.png)

Here is an example. Can you tell which is the original and which holds the watermark?

![Original](/assets/images/dog-original-.png) ![Watermarked](/assets/images/dog-watermarked-.png)

It's the second one that is watermarked, but you would never know without being told.

Here is the text hidden in the second image.

![template](/assets/images/template.png)


## Requirements and Installation

This project uses argparse and PIL to run.

```
python3 -m pip install argparse
python3 -m pip install pillow
```
NOTE: This project requires a PNG or BMP file using RGB or RGBA formatting.

WARNING: Adding a watermarked image to a Microsoft Word document and then saving it from the Word document WILL add noise to the image file that may damage the watermark.

An example command is:
```
python3 Invisible-Watermark.py -i input_file.png -t Watermark_text -f 10 -w 20 -m 0
```
