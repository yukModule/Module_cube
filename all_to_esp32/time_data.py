from weather import load
from putpic import show_words
from putpic import show_img
from weather import updatetime


def get_week_with_data(y,m,d):
    '''根据年月日计算星期几'''
    y = y - 1 if m == 1 or m == 2 else y
    m = 13 if m == 1 else (14 if m == 2 else m)
    w = (d + 2 * m + 3 * (m + 1) // 5 + y + y // 4 - y // 100 + y // 400) % 7 + 1
    return w

def main_Year_To_Date():
    s=updatetime()
    time_date=s[:10]
    show_words(time_date, 140,202, 255, 255, 255,0, 0, 0)
    T=time_date.split('-')
    w=get_week_with_data(int(T[0]),int(T[1]),int(T[2]))
    show_img(["pic/week/week1.dat",140,150,40,40])
    show_img(["pic/week/week{}.dat".format(w+1),180,150,40,40])
    time=s[10:]
    show_img(["pic/num/num{}.dat".format(int(time[0])),18,152,28,55])
    show_img(["pic/num/num{}.dat".format(int(time[1])),18+28,152,28,55])
    show_img(["pic/num/numy{}.dat".format(int(time[2])),18+28*2,152,28,55])
    show_img(["pic/num/numy{}.dat".format(int(time[3])),18+28*3,152,28,55])
