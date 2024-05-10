from machine import SoftSPI,Pin,SPI
import os,sdcard
from time import sleep

def sd_init():
    global config_dict
    config_dict = {}
    sdi = SoftSPI(baudrate=240000000,  sck=Pin(22), mosi=Pin(27), miso=Pin(26))
    sd = sdcard.SDCard(sdi, Pin(19))
    sdfile=os.VfsFat(sd)
    os.mount(sdfile,'/sd')
    dirs=os.listdir('/sd')
 
def read_config():
    '''* 读取config.txt并生成设置字典'''
    global config_dict
    with open("sd/config.txt", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            cmd_p=line.split()
            try:
                config_dict[cmd_p[0]]=cmd_p[1]
            except:
                pass
    f.close()
    print('config load')

def get_config_var():
    '''* 获取设置信息'''
    global config_dict
    return config_dict
