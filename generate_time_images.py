from utils import *
import cv2
import numpy as np
from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw 
import os

def get_background(my_image):
    return ImageDraw.Draw(my_image)

start_time = datetime.strptime("2022-01-01", "%Y-%m-%d")  # Можете выбрать любую дату
end_time = start_time + timedelta(days=1)

if 'DYNO' in os.environ:
    debug = False
    path = "/app/"
else:
    debug = True
    path = ""

def generate_image_with_text(my_image, text):
    image = get_background(my_image)
    #font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(image, text, (int(image.shape[0]*0.12), int(image.shape[1]*0.57)), font, 4, (255, 255, 255), 12, cv2.LINE_AA)
    title_font = ImageFont.truetype(f'{path}Roboto-Black.ttf', 400)
    image.text((15,15), text, (23, 33, 43), font=title_font)
    return image

while start_time < end_time:
    my_image = Image.open(f'{path}photos/robot_default.png')
    text = convert_time_to_string(start_time)
    image = generate_image_with_text(my_image, text)
    #cv2.imwrite(f"{path}time_images/{text}.jpg", image)
    my_image.save(f"{path}time_images/{text}.png")
    start_time += timedelta(minutes=1)