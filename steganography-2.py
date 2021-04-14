# Alex Luu
# 13 Apr 2021
# Python 2.7
# Python program for encoding and decoding messages in images

# PIL module used for image data extraction
from PIL import Image

# tkinter module used for file selection
import tkinter as tk
from tkinter import filedialog


# Makes a pop up for file selection
# this one has an issue where if you pick the wrong file,
# it'll give you an error after even if you pick the right file
def img_select():
    print("Please select a .png file. \n"
          "Program will terminate if wrong file type is used.")
    root = tk.Tk()
    root.withdraw()
    img = filedialog.askopenfilename()
    if img_validator(img) is True:
        return img
    else:
        return False


# validates file's extension is an image with usable format
def img_validator(name):
    if name.lower().endswith((".png", ".jpg", "jpeg")):
        return True
    else:
        return False


# Validates that a message is present
def valid_message():
    message = input("What message would you like to encode?\nNote: "
                    "Messages that are too long for the image will "
                    "be truncated.\n")
    if len(message) == 0:
        print("Empty string. Please try again:")
        valid_message()
    return message


# converts string to ASCII to binary
def string_to_binary(pre_message):
    msg_bin = []
    pre_message = str(pre_message)
    for i in pre_message:
        msg_bin.append(format(ord(i), '08b'))
    msg_bin.append('00000000')
    return msg_bin


# modifying the Blue value to hide 1 bit
def modify_pixel(pixel, value):
    value = int(value)
    b = pixel[2]
    if value == 0:
        if b % 2 == 1:
            b -= 1
    elif value == 1:
        if b % 2 == 0:
            b += 1
    new_pixel = (pixel[0], pixel[1], b)
    return new_pixel


# hid message inside pixels
def encode(image, message):
    open_img = Image.open(image, 'r')
    new_img = open_img.copy()
    msg_bin = string_to_binary(message)
    msg_len = 0
    data_len = len(msg_bin)
    hold = 0
    # for cols
    for i in range(new_img.size[0]):
        # for rows
        for j in range(new_img.size[1]):
            if hold < 8:
                value = msg_bin[msg_len][hold]
                hold += 1
            else:
                hold = 0
                msg_len += 1
                if msg_len == data_len:
                    return new_img
                else:
                    value = msg_bin[msg_len][hold]
            pixel = new_img.getpixel((i, j))
            new_pixel = modify_pixel(pixel, value)
            new_img.putpixel((i, j), new_pixel)
            new_img.putpixel((i, j), new_pixel)


# returns hidden message from image
def decode(image):
    img = Image.open(image, 'r')
    msg_str = ''
    msg_bin = ''
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = img.getpixel((i, j))
            b = pixel[2]
            if b % 2 == 1:
                msg_bin += '1'
            elif b % 2 == 0:
                msg_bin += '0'
            if len(msg_bin) == 9:
                msg_bin = msg_bin[:-1]
                if '00000000' in msg_bin:
                    return msg_str
                else:
                    to_char = int(msg_bin, 2)
                    msg_str += chr(to_char)
                    j += 1
                    msg_bin = ''


def main():
    x = "x"
    while x not in ("1", "2"):
        x = input("Enter 1 to encode. Enter 2 to decode.\n")
    if x in "1":
        message = valid_message()
        img = img_select()
        new_img = encode(img, message)
        new_name = input("Enter new image name.\n"
                         "Image will be saved in your current directory as a .png.\n")
        new_name += ".png"
        new_img.save(new_name)
    elif x in "2":
        img = False

        while img is False:
            print("Please try a different file.")
            img = img_select()
        else:
            print(decode(img))


# run program
if __name__ == "__main__":
    main()
