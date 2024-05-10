import struct
import numpy as np
from PIL import Image  # PIL灏辨槸pillow搴�


def color565(r, g, b):
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3

def main(inp,out):
    
    img = Image.open(inp)
    #print(img.format, img.size, img.mode)
    img_data = np.array(img)  # 240琛�240鍒楁湁3涓� 240x240x3
    with open(out, "wb") as f:
        for line in img_data:
            for dot in line:
                f.write(struct.pack("H", color565(*dot))[::-1])



if __name__ == '__main__':
    for i in range(1,26):
        main(f"img/img{i}.png", f"img{i}.dat")



