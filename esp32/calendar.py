from putpic import show_word_32,show_word_16
from weather import RTC
Lunar=(1,3,5,7,8,10,12)

def IsleapYear(year):
    return (year%4==0 and year%100!=0) or year%400==0
def calculation(year,month):
    sum = 0
    s_year=1990
    while s_year < year-1:
        s_year +=1
        sum += 366 if IsleapYear(s_year) else 365
    s_month=1
    while s_month<month:
        if s_month in Lunar:
            sum += 31
        elif s_month==2:
            sum += 29 if IsleapYear(year) else 28
        else:
            sum+=30
        s_month+=1
    return sum
def display(sum,year,month):
    res1=[]
    res=[]
    week=(sum+1)%7
    if month in Lunar:
        day=31
    elif month==2:
        day = 29 if IsleapYear(year) else 28
    else:
        day=30
    count = 0
    space = 0
    while space<=week:
        space+=1
        count+=1
        res1.append(' ')
        if count%7==0:
            res1=[]
    days=1
    while days<=day:
        res1.append(str(days))
        days+=1
        count+=1
        if count %7 ==0:
            res.append(res1[:])
            res1=[]
    res.append(res1[:])
    return res
def calshow():
    rtc = RTC()
    year ,month ,day=rtc.datetime()[0],rtc.datetime()[1],rtc.datetime()[2]
    days=str(day)
    sums=calculation(year,month)
    k=display(sums,year,month)
    y=0
    for i in k:
        y+=1
        x=0
        for j in i:
            show_word_16(j, 13+33*x,25+35*y, 255, 255, 255)
            if x==0 or x==6:
                show_word_16(j, 13+33*x,25+35*y, 255, 0, 72)
            if j==days:
                show_word_16(j, 13+33*x,25+35*y, 255, 178, 13)
            x+=1
    year=str(year)
    if month<10:
        month='0'+str(month)
    else:
        month=str(month)
    if day<10:
        day='0'+str(day)
    else:
        day=str(day)
    show_word_32(year+'-'+month, 63,15, 255, 219, 0)

