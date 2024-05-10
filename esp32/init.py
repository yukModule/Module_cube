import sdread
sdread.sd_init()
sdread.read_config()
from machine import freq
import machine
from weather import update, sync_ntp
from button import scan_switch
from tomato import tomato_clock
freq(240000000)

import window
window.show_start()
sync_ntp()
window.menu_app('up')

timer = machine.Timer(0)
now_t = 0
def handleInterrupt(timer):
    global now_t
    # 1s
    # 30s
    now_t += 1
    if now_t > 30:
        now_t = 0
    
    now_app, in_app = window.get_menu()
    if in_app == 1 and now_app == 5:
        tomato_clock()
        
    
    if in_app == 1 and now_app == 5 and now_t == 0:
        window.menu_app('down')
    

timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=handleInterrupt)

def main():
    while True:
        now_app, in_app = window.get_menu()
        window.menu_app(scan_switch())
        if in_app == 1 and now_app == 0:
            window.show_aim()

