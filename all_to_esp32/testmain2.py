from machine import I2C,Pin
import mpu6050
from time import sleep_ms
import putpic
import time
import weather
import time_data
import utime
import machine#导入machine模块
from calendar import calshow
from sdread import sdshow

i2c = I2C(sda=Pin(32), scl=Pin(33))
k_angle = 180
angle_x = 0
angle_y = 0
angle_garget = 0
menu_show=6
menu=''
interruptCounter = 0
totalInterruptsCounter = 0
sdpicCounter = 0
timer = machine.Timer(0)
switch=False
cmd=''
GTD_m,GTD_s=25,0
GTD_rest=True

def handleInterrupt(timer):
    global interruptCounter,totalInterruptsCounter,GTD_m,GTD_s,GTD_rest,sdpicCounter
    totalInterruptsCounter+=1
    interruptCounter +=1
    if menu=='sdpic':
        sdpicCounter +=1
        if sdpicCounter>5:
            sdpicCounter=0
            sdshow()
    if menu=='GTD':
        if GTD_s==-1:
            GTD_s=59
            GTD_m-=1
            if GTD_m==-1:
                if GTD_rest:
                    GTD_m,GTD_s=5,0
                    GTD_rest=False
                else:
                    GTD_m,GTD_s=25,0
                    GTD_rest=True
            if GTD_m<10:
                strm='0'+str(GTD_m)
            else:
                strm=str(GTD_m)
            putpic.show_img(["pic/num/numy{}.dat".format(int(strm[0])),92,92,28,55])
            putpic.show_img(["pic/num/numy{}.dat".format(int(strm[1])),92+28,92,28,55])
        if GTD_s<10:
            strs='0'+str(GTD_s)
        else:
            strs=str(GTD_s)
        putpic.show_word(strs, 149,108, 5, 229, 51,0, 0, 0)
        GTD_s-=1
        
    if interruptCounter>1:
        interruptCounter=0
    if totalInterruptsCounter>60:
        if menu=='main':
            time_data.main_Year_To_Date()
        totalInterruptsCounter=0
timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=handleInterrupt)

putpic.show_rectangle(0,0,240,240,12,205, 255)
putpic.show_rectangle(10,10,220,220,0,0,0)
putpic.show_img(['start.dat',10,59,220,122])

accel = mpu6050.accel(i2c)
accel_dict = accel.get_values()
print(accel_dict)

# 如果不需要外部供电启动，将下面一行取消注释
weather.sync_ntp()

while True:
    accel_dict = accel.get_values()
    r,p,y=accel_dict['AcZ']/ 32768 * k_angle-90,accel_dict['AcY']/ 32768 * k_angle,accel_dict['AcX']/ 32768 * k_angle
    sleep_ms(1000 // 25)
    if p>20 and -20<y<20 and switch:
        switch=False
        if menu=='':
            if menu_show>1:
                menu_show-=1
            else:
                menu_show=11
            putpic.show_img(['pic/app/app{}.dat'.format(menu_show),80,80,80,80])
    if p<-20 and -20<y<20 and switch:
        switch=False
        if menu=='':
            if menu_show<11:
                menu_show+=1
            else:
                menu_show=1
            putpic.show_img(['pic/app/app{}.dat'.format(menu_show),80,80,80,80])
    if y>20 and -20<p<20 and switch:
        switch=False
        putpic.show_rectangle(10,10,220,220,0,0,0)
        putpic.show_img(['pic/app/app{}.dat'.format(menu_show),80,80,80,80])
        cmd='up'
        menu=''
    if y<-20 and -20<p<20 and switch and menu=='':
        switch=False
        putpic.show_rectangle(10,10,220,220,0,0,0)
        cmd='down'
    if -15<p<15 and -15<y<15:
        switch=True
    if cmd=='down' and menu=='':
        if menu_show==3:
            menu='sdpic'
            sdshow()
        if menu_show==5:
            menu='calendar'
            calshow()
        if menu_show==6:
            menu='main'
            time_data.main_Year_To_Date()
            weather.main_weather()
        if menu_show==7:
            menu='temp'
            weather.temp_5d()
        if menu_show==8:
            menu='GTD'
            putpic.show_img(["pic/num/numy2.dat",92,92,28,55])
            putpic.show_img(["pic/num/numy5.dat",92+28,92,28,55])
            putpic.show_word('00', 149,108, 5, 229, 51,0, 0, 0)
            GTD_m,GTD_s=25,0
        if menu_show==10:
            menu='time_ud'
            putpic.show_word('wait', 87,105, 255, 255, 255,0, 0, 0)
            weather.sync_ntp()
            putpic.show_img(['pic/app/app12.dat',80,80,80,80])
        if menu_show==11:
            menu='weather_ud'
            putpic.show_word('wait', 87,105, 255, 255, 255,0, 0, 0)
            weather.update()
            putpic.show_img(['pic/app/app12.dat',80,80,80,80])
        cmd=''
    
