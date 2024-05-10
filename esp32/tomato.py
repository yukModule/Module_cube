from putpic import show_img

work_or_rest = 1
work = 25
rest = 5
now_time_m = 25
now_time_s = 0

def reset_clock():
    global work, rest, now_time_m, now_time_s, work_or_rest
    work_or_rest = 1
    work = 25
    rest = 5
    now_time_m = 25
    now_time_s = 0

def tomato_clock():
    global work, rest, now_time_m, now_time_s, work_or_rest
    now_time_s -= 1
    if now_time_s < 0:
        now_time_s = 59
        if now_time_m > 0 :
            now_time_m -= 1
        else:
            work_or_rest = 1 - work_or_rest
            if work_or_rest:
                now_time_m = work
                now_time_s = 0
            else:
                now_time_m = rest
                now_time_s = 0
            
    time_m = str(now_time_m)
    time_s = str(now_time_s)
    if now_time_m < 10:
        time_m = '0' + time_m
    if now_time_s < 10:
        time_s = '0' + time_s
        
    show_img("pic/num/num{}.dat".format(int(time_m[0])),55,92,28,55)
    show_img("pic/num/num{}.dat".format(int(time_m[1])),55+28,92,28,55)
    show_img("pic/num/numy{}.dat".format(int(time_s[0])),129,92,28,55)
    show_img("pic/num/numy{}.dat".format(int(time_s[1])),129+28,92,28,55)
