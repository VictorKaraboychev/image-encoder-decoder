from PIL import Image
from itertools import product
import struct
import random

def setBit(byte, bit, offset):
    byte >>= 1 + offset
    byte <<= 1 + offset
    return byte | bit

def getBit(byte, offset):
    return int(byte & 2**offset != 0)

def stringToInt(string):
    int_value = 0
    for i in range(len(string)):
        int_value += ord(string[i]) * 256**i
    return int_value

# DATA STRUCTURE
# 0-7: 1x encoded, 1 byte responsible for denoting the encoding density
# 8-71: 8 bytes denoting the length of the stored data
# 72-135: 8 bytes denoting the file suffix
# 136+: encoded data

def encode(image, filedata, suffix, set_data_density, stripe):
    data = bytearray()
    data.append(set_data_density)
    data.extend(struct.pack('>Q', len(filedata)))
    data.extend(struct.pack('>Q', stringToInt(suffix)))
    data.extend(filedata)

    new_image = Image.new("RGBA", image.size, (255, 255, 255, 255))

    data_density = 0
    current_bit = 0
    for y, x in product(range(image.height), range(image.width)):
        image_data = image.getpixel((x, y))

        new_image_data = []
        for c in range(4):
            modified_channel = 255
            if (c < 3): modified_channel = image_data[c]

            for o in range(data_density, -1, -1):
                bit = getBit(modified_channel, o)
                if (current_bit // 8 < len(data) or stripe):
                    byte = data[current_bit // 8]     
                    if (isinstance(byte, str)): byte = ord(byte)

                    bit = getBit(byte, 7 - (current_bit % 8))
                else:
                    bit = random.randint(0, 1)
                modified_channel = setBit(modified_channel, bit * 2**o, o)
                current_bit += 1

                if (current_bit == 8):
                    data_density = set_data_density

            new_image_data.append(modified_channel)
        new_image.putpixel((x, y), tuple(new_image_data))
    return new_image