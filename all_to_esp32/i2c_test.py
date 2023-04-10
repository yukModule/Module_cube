from machine import UART,Pin
import utime

# 初始化一个UART对象
uart = UART(2, baudrate=9600, rx=13,tx=12,timeout=10)
while True:
    if uart.any():
        bin_data = uart.readline()
        # 将手到的信息打印在终端
        #print('Echo Byte: {}'.format(bin_data))
        # 将字节数据转换为字符串 字节默认为UTF-8编码
        print('Echo String: {}'.format(bin_data.decode()))



