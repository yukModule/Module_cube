from machine import Pin
from sdread import get_config_var
mirror_var = get_config_var()['mirror']

if mirror_var == '0':
    up = Pin(35, Pin.IN) #定义输入
    down = Pin(33, Pin.IN) #定义输入
    left = Pin(32, Pin.IN) #定义输入
    right = Pin(34, Pin.IN) #定义输入
else:
    up = Pin(33, Pin.IN) #定义输入
    down = Pin(35, Pin.IN) #定义输入
    left = Pin(34, Pin.IN) #定义输入
    right = Pin(32, Pin.IN) #定义输入

def scan_switch():
    if up.value() == 1:
        return 'up'
    if down.value() == 1:
        return 'down'
    if left.value() == 1:
        return 'left'
    if right.value() == 1:
        return 'right'
    return 0
