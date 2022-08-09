import random
import argparse
from argparse import RawTextHelpFormatter
from PIL import Image, ImageDraw, ImageFont


def generate_template(original_img, text_to_add, path_to_image, font_size, num_of_watermarks):

    #Opening Image & Creating New Text Layer
    new_img = Image.new('RGB', original_img.size, (255, 255, 255))

    #Creating Text
    font = ImageFont.truetype("arial.ttf", font_size)

    #Creating Draw Object
    #this is what tells the draw tool which image to use
    draw = ImageDraw.Draw(new_img)

    #Positioning of Text
    width, height = original_img.size

    #Loop for Multiple Watermarks
    y = 1
    bo = 0 #this is a check to see if we have reached the top or bottom
    for i in range(num_of_watermarks):

        if y > height: #if y is past the top of the image start subracting instead of adding
            bo = 1
        elif y < 0:
            bo = 0

        if bo == 0:
            y += random.randrange(0, int(height / 8), 19) + random.randint(0, 100)

        else:
            y -= random.randrange(0, int(height / 8), 19) + random.randint(0, 100)

        x = random.randint(0, width - 200)
        draw.text((x, y), text_to_add, fill=(0, 0, 0), font=font)

    #Combining both layers and saving new image
    #watermarked = Image.alpha_composite(original_img, new_img)
    new_img.save('template_' + path_to_image)
    return new_img

def generate_watermark(path_to_image, text_to_add, font_size, num_of_watermarks):
    #read all the data from the image
    try: #ensure the image exists on disk
        original_img = Image.open(path_to_image)

    except FileNotFoundError as e:
        print(e)
        exit(1)

    print("Image mode is: " + str(original_img.mode)  + " for " + path_to_image)
    if original_img.mode != 'RGB': #check to see if image is rgb
        original_img = original_img.convert('RGB')
        print("Image mode is NOW: " + str(original_img.mode) + " for " + path_to_image)

    #get the size of the image
    width, height = original_img.size

    #generate the template to use
    template = generate_template(original_img, text_to_add, path_to_image, font_size, num_of_watermarks)

    #loop through each pixel checking the template for white or black pixels and
    #modifying the original_img to reflect those changes
    #key white oi_r needs to be even black oi_r needs to be odd
    #oi_r = original_image red make sense?
    for row in range(height):
        for col in range(width):
            r, g, b = template.getpixel((col, row)) #r g b is for the template image
            oi_r, oi_g, oi_b = original_img.getpixel((col, row)) #oi_r oi_g oi_b is for the original image

            if r > 150: #logic tree if the r value is over 150 (closer to white than black) were making it a white pixel
                if oi_r % 2 != 0: #check if the pixel is odd or even and if it is odd we need to add or subtract 1
                    if oi_r + 1 > 255: #if adding 1 pushes over 255 (the max limit for rgb) subtract one
                        oi_r = oi_r - 1
                    else:
                        oi_r = oi_r + 1

            else:
                if oi_r % 2 == 0: #if the r value is even we need to make it odd by adding or subtracting 1
                    if oi_r + 1 > 255: #if adding 1 pushes over 255 (the max limit for rgb) subtract one
                        oi_r = oi_r - 1
                    else:
                        oi_r = oi_r + 1

            #no put the pixel on the image
            original_img.putpixel((col, row), (oi_r, oi_g , oi_b))

    original_img.save('download_' + str(path_to_image))

def check_watermark(path_to_image):

    #open the image
    try:  #ensure the image exists on disk
        original_img = Image.open(path_to_image)

    except FileNotFoundError as err:
        print(err)
        exit(1)

    print("Image mode is: " + str(original_img.mode) + " for " + path_to_image)
    if original_img.mode != 'RGB': #check to see if image is rgb
        original_img = original_img.convert('RGB') #if its not make it rgb
        print("Image mode is NOW: " + str(original_img.mode) + " for " + path_to_image)

    #generate a white canvas that will hold the extracted watermark
    water_check = Image.new('RGB', original_img.size, (255, 255, 255))

    #get the width and height
    width, height = original_img.size

    #loop through each pixel in the image if the r value is even it is white if it is odd it is black
    #then append these color changes to the new image water_check
    for row in range(height):
        for col in range(width):
            r, g, b = original_img.getpixel((col, row)) #r g b is for the original_img

            if r % 2 != 0: #check to see if the red pixel is odd (if it is add a black pixel to water_check)
                water_check.putpixel((col, row), (0, 0, 0))

    #save the watermark
    water_check.save('reterived_watermark_' + str(path_to_image))




def main():

    #arguments
    parser = argparse.ArgumentParser(description='Image Watermarker\n\n#Requires an RGB or RGBA formatted PNG or BMP image', epilog="modes:\n  0 : Watermark\n  1 : Check Watermark", formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--input', help='Input file name', required=False)
    parser.add_argument('-iF', '--input-file', help='Input for multiple files in a text file', required=False)
    parser.add_argument('-m', '--mode', choices=['0', '1'], help='Mode fore the script', required=True)
    parser.add_argument('-t', '--text', help='Watermark text', required=False)
    parser.add_argument('-f', '--font-size', type=int, help='Font size (Default 30)', required=False)
    parser.add_argument('-w', '--watermark-num', type=int, help='Number of times to watermark the image (Default 10)', required=False)
    args = parser.parse_args()

    #Checking and setting default values
    if args.font_size is None:
        args.font_size = 30

    if args.watermark_num is None:
        args.watermark_num = 10

    if args.input is not None: #if the input exists
        if args.mode == '0': #if we are watermarking the image
            if args.text is not None: #check to see if they supplied us text
                generate_watermark(args.input, args.text, args.font_size, args.watermark_num)

            else:
                print("Error: No watermark text supplied.")
                exit(1)

        elif args.mode == '1': #if were just extracting the watermark
            check_watermark(args.input)

    elif args.input_file is not None: #if we are doing multiple images
        items = []

        try:#ensure there are no errors
            with open(args.input_file, 'r') as f: #open the input file
                items = f.readlines() #read its contents into an array
                f.close()

        except FileNotFoundError as err:
            print(err)
            exit(1)

        if args.mode == '0': #if were watermarking images
            if args.text is not None: #and we have text
                for item in items: #loop through them
                    generate_watermark(item.strip('\n'), args.text, args.font_size, args.watermark_num)

            else:
                print("Error: No watermark text supplied.")
                exit(1)

        elif args.mode == '1': #if were checking
            for item in items: #loop through them
                check_watermark(item.strip('\n'))

    else: #no file :(
        print("Error: No file to watermark or check")
        exit(1)

if __name__ == "__main__":
    main()

