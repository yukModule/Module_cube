import ujson
import network
import urequests
import uzlib as zlib
import time
import putpic
from machine import RTC
SSID = "mkm_iqoowifi"                  #WiFi名称
PASSWORD = "abc123123abc1237"            #WiFi密码

FTEXT    = 1
FHCRC    = 2
FEXTRA   = 4
FNAME    = 8
FCOMMENT = 16

def decompress(data):
    assert data[0] == 0x1f and data[1] == 0x8b
    assert data[2] == 8
    flg = data[3]
    assert flg & 0xe0 == 0
    i = 10
    if flg & FEXTRA:
        i += data[11] << 8 + data[10] + 2
    if flg & FNAME:
        while data[i]:
            i += 1
        i += 1
    if flg & FCOMMENT:
        while data[i]:
            i += 1
        i += 1
    if flg & FHCRC:
        i += 2
    return zlib.decompress(memoryview(data)[i:], -15)

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PASSWORD)
        i = 1
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            i += 1
            time.sleep(1)


def update():
    do_connect()
    url='https://devapi.qweather.com/v7/weather/7d?location=!!!&key=!!!'
    res=urequests.get(url)
    data=decompress(res.content).decode()
    dic=ujson.loads(data)
    urlnow='https://devapi.qweather.com/v7/weather/now?location=!!!&key=!!!'
    resnow=urequests.get(urlnow)
    datanow=decompress(resnow.content).decode()
    dicnow=ujson.loads(datanow)
    with open("save.txt","w") as f:
        f.write("".join(dicnow['now']['temp'])+"\n")
        f.write("".join(dicnow['updateTime'])+"\n")
        f.write("".join(dic['daily'][0]['tempMax'])+"\n")
        f.write("".join(dic['daily'][0]['tempMin'])+"\n")
        f.write("".join(dic['daily'][0]['textDay'])+"\n")
        f.write("".join(dic['daily'][1]['tempMax'])+"\n")
        f.write("".join(dic['daily'][1]['tempMin'])+"\n")
        f.write("".join(dic['daily'][1]['textDay'])+"\n")
        f.write("".join(dic['daily'][2]['tempMax'])+"\n")
        f.write("".join(dic['daily'][2]['tempMin'])+"\n")
        f.write("".join(dic['daily'][2]['textDay'])+"\n")
        f.write("".join(dic['daily'][3]['tempMax'])+"\n")
        f.write("".join(dic['daily'][3]['tempMin'])+"\n")
        f.write("".join(dic['daily'][3]['textDay'])+"\n")
        f.write("".join(dic['daily'][4]['tempMax'])+"\n")
        f.write("".join(dic['daily'][4]['tempMin'])+"\n")
        f.write("".join(dic['daily'][4]['textDay'])+"\n")
        f.write("".join(dicnow['now']['humidity'])+"\n")
        f.write("".join(dicnow['now']['windScale'])+"\n")

def sync_ntp():
    do_connect()
    """通过网络校准时间"""
    import ntptime
    ntptime.NTP_DELTA = 3155644800
    ntptime.host = 'ntp1.aliyun.com'
    while True:   #时间校准
        try:
            print('time ing')
            ntptime.settime()
            print('time ok')
            break;
        except:
            print('time no')
            time.sleep(1)


def load():
    date_list=[]
    with open("save.txt", "r") as f:
        for i in range(19):
            date = f.readline()
            date_list.append(date[:-1])
    return date_list

def main_weather():
    weather_date=load()
    putpic.show_img(["pic/pic/ico25.dat",130,40,40,40])
    putpic.show_word("{}".format(weather_date[18]), 180,50, 255, 255, 255,0, 0, 0)
    putpic.show_img(["pic/pic/ico26.dat",130,90,40,40])
    putpic.show_word("{}%".format(weather_date[17]), 170,100, 0, 90, 255,0, 0, 0)
    putpic.show_word("{}.5'C".format(weather_date[0]), 15,102, 255, 255, 255,0, 0, 0) 
    k=['多云','晴','阴','小雨','中雨','大雨','冻雨','阵雨']
    for i in range(9):
        if k[i]==weather_date[4]:
            putpic.show_img(["pic/weather/weather{}.dat".format(i+1),17,15,90,90])
            return
        
    
def temp_5d():
    k=['多云','晴','阴','小雨','中雨','大雨','冻雨','阵雨']
    weather_date=load()
    maxtemp=[int(weather_date[2]),int(weather_date[5]),int(weather_date[8]),int(weather_date[11]),int(weather_date[14])]
    mintemp=[int(weather_date[3]),int(weather_date[6]),int(weather_date[9]),int(weather_date[12]),int(weather_date[15])]
    weathertext=[weather_date[4],weather_date[7],weather_date[10],weather_date[13],weather_date[16]]
    maxt=max(maxtemp)
    mint=min(mintemp)
    rate=90/(maxt-mint)
    for i in range(4):
        putpic.bias(20+i*50,105+int(rate*(maxt-maxtemp[i])),70+i*50,105+int(rate*(maxt-maxtemp[i+1])),5,255,255,255)
        putpic.bias(20+i*50,105+int(rate*(maxt-mintemp[i])),70+i*50,105+int(rate*(maxt-mintemp[i+1])),5,255,255,255)
    for i in range(5):
        putpic.show_words(str(maxtemp[i]), 13+i*50,90, 255, 255, 255,0, 0, 0)
        putpic.show_words(str(mintemp[i]), 13+i*50,200, 255, 255, 255,0, 0, 0)
        for j in range(9):
            if k[j]==weathertext[i]:
                putpic.show_img(["pic/pic/ico{}.dat".format(j+1),13+43*i,30,40,40])
                break
            
def updatetime():
    rtc = RTC()
    n,y,r,h,m=rtc.datetime()[0],rtc.datetime()[1],rtc.datetime()[2],rtc.datetime()[4],rtc.datetime()[5]
    if(m==0):
        update()
        main_weather()
    n=str(n)
    if y<10:
        y='0'+str(y)
    else:
        y=str(y)
    if r<10:
        r='0'+str(r)
    else:
        r=str(r)
    if h<10:
        h='0'+str(h)
    else:
        h=str(h)
    if m<10:
        m='0'+str(m)
    else:
        m=str(m)
    return n+'-'+y+'-'+r+h+m
