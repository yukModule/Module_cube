from machine import Pin, SPI
import st7789_itprojects
from romfonts import vga2_bold_16x32 as font32
from romfonts import vga1_8x16 as font16
import random
from math import sqrt
from sdread import get_config_var
import random

tft = st7789_itprojects.ST7889_Image(SPI(2, 240000000), dc=Pin(2), cs=Pin(5), rst=Pin(15))
mirror_var = get_config_var()['mirror']
tft.rotation(int(mirror_var))
tft.vscrdef(20,100,20)

tft.fill(st7789_itprojects.color565(0, 0, 0))  # 背景设置为黑色
def show_rectangle(x,y,w,h,r,g,b):
    '''矩形填充'''
    tft.fill_rectangle(x,y,w,h, st7789_itprojects.color565(r,g,b))
def reput():
    '''清屏'''
    tft.fill(st7789_itprojects.color565(0, 0, 0))
def show_word_32(word,x,y,r,g,b):
    '''显示32像素英文字符'''
    tft.text(font32, word,x,y,st7789_itprojects.color565(r,g,b), st7789_itprojects.color565(0,0,0))
def show_word_16(word,x,y,r,g,b):
    '''显示16像素英文字符'''
    tft.text(font16, word,x,y,st7789_itprojects.color565(r,g,b), st7789_itprojects.color565(0,0,0))
def sdshow():
    '''随机显示sd卡内的图片'''
    n = int(get_config_var()['pic_num'])
    show_img(f'sd/img{random.randrange(1, n, 1)}.dat', 10, 10, 220, 220)
def bias(x1,y1,x2,y2,w,r,g,b):
    '''绘制温度折线'''
    yn=xn=0
    k=(y2-y1)/(x2-x1)
    if k>0:
        for i in range(x2-x1):
            if(int(k*i)>yn):
                show_rectangle(x1+xn-1,y1+yn,i-xn+1,int((w/k*sqrt(1+k*k)-i+xn)*k),r,g,b)
                xn=i
                yn=int(k*i)
        if (i!=yn):
            show_rectangle(x1+xn-1,y1+yn,i-xn+1,int((w/k*sqrt(1+k*k)-i+xn)*k),r,g,b)
    if k<0:
        for i in range(x2-x1):
            if(int(k*i)<yn):
                show_rectangle(x1+xn-1,y1+yn,i-xn+1,int((w/k*sqrt(1+k*k)-i+xn)*k)-2,r,g,b)
                xn=i
                yn=int(k*i)
        if (i!=yn):
            show_rectangle(x1+xn-1,y1+yn,i-xn+1,int((w/k*sqrt(1+k*k)-i+xn)*k),r,g,b)
    if k==0:
        show_rectangle(x1,y1,x2-x1,w-1,r,g,b)

def show_img(pic,x,y,w,h):
    '''显示图片'''
    with open(pic, "rb") as f:
        for row in range(h): 
            buffer = f.read(w*2)
            tft.show_img(x, row+y, w+x, row+y, buffer)
    f.close()

def show_aim():
    col_max = tft.width - font16.WIDTH*6
    row_max = tft.height - font16.HEIGHT
    for _ in range(10):
        tft.text(
            font16,
            "Hello!",
            random.randint(0, col_max),
            random.randint(0, row_max),
            st7789_itprojects.color565(random.getrandbits(8),random.getrandbits(8),random.getrandbits(8)),
            st7789_itprojects.color565(random.getrandbits(8),random.getrandbits(8),random.getrandbits(8))
        )

