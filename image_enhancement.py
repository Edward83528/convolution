# -*- coding: utf-8 -*-
"""
影像處理-image_enhancement
"""
# 引入套件
import os
from PIL import Image, ImageFont, ImageDraw

def show(title, img):
    font_color = (224, 60, 138)
    font_size = 30
    font = ImageFont.truetype("arial.ttf", font_size)
    tmp_img = img.copy()
    d = ImageDraw.Draw(tmp_img)
    d.text((20, 20), title, font=font, fill=font_color)
    tmp_img.show()

def convolution(x, y, arr, pixels, pixels2):
    idx = 0
    r = int(pixels[x-1, y-1][idx]*arr[0][0] + pixels[  x, y-1][idx]*arr[1][0] + pixels[x+1, y-1][idx]*arr[2][0]\
          + pixels[x-1, y  ][idx]*arr[0][1] + pixels[  x, y  ][idx]*arr[1][1] + pixels[x+1, y  ][idx]*arr[2][1]\
          + pixels[x-1, y+1][idx]*arr[0][2] + pixels[  x, y+1][idx]*arr[1][2] + pixels[x+1, y+1][idx]*arr[2][2])
    idx = 1
    g = int(pixels[x-1, y-1][idx]*arr[0][0] + pixels[  x, y-1][idx]*arr[1][0] + pixels[x+1, y-1][idx]*arr[2][0]\
          + pixels[x-1, y  ][idx]*arr[0][1] + pixels[  x, y  ][idx]*arr[1][1] + pixels[x+1, y  ][idx]*arr[2][1]\
          + pixels[x-1, y+1][idx]*arr[0][2] + pixels[  x, y+1][idx]*arr[1][2] + pixels[x+1, y+1][idx]*arr[2][2])
    idx = 2
    b = int(pixels[x-1, y-1][idx]*arr[0][0] + pixels[  x, y-1][idx]*arr[1][0] + pixels[x+1, y-1][idx]*arr[2][0]\
          + pixels[x-1, y  ][idx]*arr[0][1] + pixels[  x, y  ][idx]*arr[1][1] + pixels[x+1, y  ][idx]*arr[2][1]\
          + pixels[x-1, y+1][idx]*arr[0][2] + pixels[  x, y+1][idx]*arr[1][2] + pixels[x+1, y+1][idx]*arr[2][2])
    pixels2[x, y] = (r, g, b)


def image_add(pixels, pixels2):
    image = Image.new('RGB', size, "black")
    pixels3 = image.load()
    for x in range(size[0]-2):
        for y in range(size[1]-2):
            pixels3[x, y] = (pixels[x, y][0]+pixels2[x, y][0], pixels[x, y][1]+pixels2[x, y][1], pixels[x, y][2]+pixels2[x, y][2])
    return image

def image_mul(pixels,pixels2):
    image = Image.new( 'RGB', size, "black")
    pixels3 = image.load()
    for x in range(size[0]-2):
        for y in range(size[1]-2):
            pixels3[x,y] = (int(pixels[x,y][0]*pixels2[x,y][0]/255),int(pixels[x,y][1]*pixels2[x,y][1]/255),int(pixels[x,y][2]*pixels2[x,y][2]/255))
    return image

# 載入原圖
path = 'img/view.jpg' # 圖片路徑
im = Image.open(os.path.abspath(path))
size = im.size
show("0 原圖",im)

# Laplacian
arr = [[ -1.,  -1., -1.],
       [ -1.,   8., -1.],
       [ -1.,  -1., -1.]]
im1 = Image.new( 'RGB', size, "black")
pixels = im.load() 
pixels2 = im1.load() 
for i in range(size[0]-2):
  for j in range(size[1]-2):
     convolution(i+1,j+1,arr,pixels,pixels2)
show("1 Laplacian Mask",im1)

# 原始影像直接銳利
im2 = image_add(pixels,pixels2)
show("2 (0)和（1)相加",im2)

# X方向一階微分
arr = [[ -1.,  0,   1],
       [ -2.,  0.,  2],
       [ -1.,  0.,  1]]
im3_x = Image.new( 'RGB', size, "black")
pixels2 = im3_x.load() 
for i in range(size[0]-2):
  for j in range(size[1]-2):
     convolution(i+1,j+1,arr,pixels,pixels2)
 
# Ｙ方向一階微分
arr = [[  1.,  2,   1],
       [  0.,  0.,  0],
       [ -1., -2., -1]]
im3_y = Image.new( 'RGB', size, "black")
pixels3 = im3_y.load()
for i in range(size[0]-2):
  for j in range(size[1]-2):
     convolution(i+1,j+1,arr,pixels,pixels3)

# ＸＹ方像取絕對值相加
for x in range(size[0]-2):
    for y in range(size[1]-2):
        pixels2[x,y] = (abs(pixels2[x,y][0]),abs(pixels2[x,y][1]),abs(pixels2[x,y][2]))
        pixels3[x,y] = (abs(pixels3[x,y][0]),abs(pixels3[x,y][1]),abs(pixels3[x,y][2]))
im3 = image_add(pixels2,pixels3)
show("3 (0)一階微分",im3)

# 將一階微分結果模糊去雜訊
arr = [[ 1/9.,  1/9.,  1/9.],
       [ 1/9.,  1/9.,  1/9.],
       [ 1/9.,  1/9.,  1/9.]]
im4 = Image.new( 'RGB', size, "black")
pixels = im3.load()
pixels2 = im4.load()
for i in range(size[0]-2):
  for j in range(size[1]-2):
     convolution(i+1,j+1,arr,pixels,pixels2)
show("4 (3)模糊後結果（去雜訊）",im4)

pixels = im2.load()
im5 = image_mul(pixels,pixels2)
show("5 (4)正規化乘上（2）",im5)

im6 = image_add(im.load(),im5.load())
show("6 (5)加上原始影像（0）無雜訊",im6)

# 4*1+0
pixels = im1.load()
im7 = image_mul(pixels2,pixels)
im7 = image_add(im7.load(),im.load())
show("7 (4)正規化乘上（1）加上（0）",im7)