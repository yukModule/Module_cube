from machine import SoftSPI,Pin,SPI
import os,sdcard
import random
from putpic import show_img

sdi = SoftSPI(baudrate=8000000,  sck=Pin(22), mosi=Pin(27), miso=Pin(26))
sd = sdcard.SDCard(sdi, Pin(19))
sdfile=os.VfsFat(sd)
os.mount(sdfile,'/sd')
dirs=os.listdir('/sd')
n=0
for file in dirs:
    n+=1
def sdshow():
    show_img(['sd/img{}.dat'.format(random.randrange(1,n-1,1)),10,10,220,220])
