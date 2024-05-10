from putpic import show_img, show_word_32, show_word_16, sdshow, reput, show_aim
from weather import load, main_weather, temp_5d
from weather import updatetime, update, sync_ntp
from calendar import calshow
from sdread import read_config
from time import sleep
import tomato


def show_reload():
    show_word_32('wait', 87,105, 255, 255, 255)
    read_config()
    show_img('pic/app/app12.dat',80,80,80,80)
    
def show_game():
    pass

def show_tomato():
    tomato.reset_clock()
    tomato.tomato_clock()

def show_range_pic():
    sleep(0.1)
    sdshow()

def show_reset_time():
    show_word_32('wait', 87,105, 255, 255, 255)
    sync_ntp()
    show_img('pic/app/app9.dat',80,80,80,80)

def show_updata():
    show_word_32('wait', 87,105, 255, 255, 255)
    update()
    show_img('pic/app/app9.dat',80,80,80,80)

def get_week_with_data(y,m,d):
    '''根据年月日计算星期几'''
    y = y - 1 if m == 1 or m == 2 else y
    m = 13 if m == 1 else (14 if m == 2 else m)
    w = (d + 2 * m + 3 * (m + 1) // 5 + y + y // 4 - y // 100 + y // 400) % 7 + 1
    return w

def main_Year_To_Date():
    s=updatetime()
    time_date=s[:10]
    show_word_16(time_date, 145,205, 255, 255, 255)
    T=time_date.split('-')
    w=get_week_with_data(int(T[0]),int(T[1]),int(T[2]))
    show_img("pic/week/week1.dat",142,152,40,40)
    show_img("pic/week/week{}.dat".format(w+1),182,152,40,40)
    time=s[10:]
    show_img("pic/num/num{}.dat".format(int(time[0])),15,158,28,55)
    show_img("pic/num/num{}.dat".format(int(time[1])),15+28,158,28,55)
    show_img("pic/num/numy{}.dat".format(int(time[2])),15+28*2,158,28,55)
    show_img("pic/num/numy{}.dat".format(int(time[3])),15+28*3,158,28,55)

def show_main():
    #show_img('pic/weather/weather1.dat',10,10,90,90)
    main_weather()
    main_Year_To_Date()

def show_menu(n):
    show_img('pic/app/app{}.dat'.format(n),80,80,80,80)

def show_start():
    show_img('start.dat', 10, 59, 220, 122)

def show_calendar():
    calshow()

def show_5d():
    temp_5d()

app_list = [show_game, show_range_pic, show_calendar, show_main, show_5d, show_tomato, show_reset_time, show_updata]
in_app = 0
now_app = 0

def get_menu():
    global now_app, in_app
    return now_app, in_app

def menu_app(sw):
    global app_list, now_app, in_app
    if sw == 0:
        return
    # 菜单选择
    if sw == 'right' and in_app == 0:
        now_app += 1
        if now_app >= 8:
            now_app = 0
        show_menu(now_app+1)
    elif sw == 'left' and in_app == 0:
        now_app -= 1
        if now_app <= -1:
            now_app = 7
        show_menu(now_app+1)
    # 进入/退出程序
    elif sw == 'up':
        reput()
        show_menu(now_app+1)
        in_app = 0
    elif sw == 'down':
        if in_app == 0:
            reput()
        app_list[now_app]()
        in_app = 1
    sleep(0.5)
    