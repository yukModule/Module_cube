from machine import Pin, SPI
import st7789_itprojects
from romfonts import vga2_bold_16x32 as font32
from romfonts import vga1_8x16 as font16
import random
from math import sqrt

tft = st7789_itprojects.ST7889_Image(SPI(2, 80000000), dc=Pin(2), cs=Pin(5), rst=Pin(15))

tftw = st7789_itprojects.ST7789(SPI(2, 80000000), dc=Pin(2), cs=Pin(5), rst=Pin(15))

tft.rotation()
tft.vscrdef(20,100,20)

tft.fill(st7789_itprojects.color565(0, 0, 0))  # 背景设置为黑色

def show_rectangle(x,y,w,h,r,g,b):
    tft.fill_rectangle(x,y,w,h, st7789_itprojects.color565(r,g,b))
def reput():
    tft.fill(st7789_itprojects.color565(0, 0, 0))
def show_word(word,x,y,r1,g1,b1,r2,g2,b2):
    tftw.text(font32, word,x,y,st7789_itprojects.color565(r1,g1,b1), st7789_itprojects.color565(r2,g2,b2))
def show_words(word,x,y,r1,g1,b1,r2,g2,b2):
    tftw.text(font16, word,x,y,st7789_itprojects.color565(r1,g1,b1), st7789_itprojects.color565(r2,g2,b2))

def show_img(plist):
    pic,picx,picy,picw,pich=plist[0],plist[1],plist[2],plist[3],plist[4]
    with open(pic, "rb") as f:
        for row in range(pich): 
            buffer = f.read(picw*2)
            tft.show_img(picx, row+picy, picw+picx, row+picy, buffer)
    f.close()

def bias(x1,y1,x2,y2,w,r,g,b):
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
   

