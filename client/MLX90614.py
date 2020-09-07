"""
MLX90614 driver. 
You might need to enter this command on your Raspberry Pi:
echo "Y" > /sys/module/i2c_bcm2708/parameters/combined
(I've put it in my rc.local so it's executed each bootup)
"""

import smbus
import time
from time import sleep

class MLX90614():

    MLX90614_RAWIR1=0x04
    MLX90614_RAWIR2=0x05
    MLX90614_TA=0x06
    MLX90614_TOBJ1=0x07
    MLX90614_TOBJ2=0x08

    MLX90614_TOMAX=0x20
    MLX90614_TOMIN=0x21
    MLX90614_PWMCTRL=0x22
    MLX90614_TARANGE=0x23
    MLX90614_EMISS=0x24
    MLX90614_CONFIG=0x25
    MLX90614_ADDR=0x0E
    MLX90614_ID1=0x3C
    MLX90614_ID2=0x3D
    MLX90614_ID3=0x3E
    MLX90614_ID4=0x3F

    comm_retries = 5
    comm_sleep_amount = 0.1

    def __init__(self, address=0x5a, bus_num=1):
        self.bus_num = bus_num
        self.address = address
        self.bus = smbus.SMBus(bus=bus_num)

    def read_reg(self, reg_addr):
        for i in range(self.comm_retries):
            try:
                return self.bus.read_word_data(self.address, reg_addr)
            except IOError as e:
                #"Rate limiting" - sleeping to prevent problems with sensor 
                #when requesting data too quickly
                sleep(self.comm_sleep_amount)
        #By this time, we made a couple requests and the sensor didn't respond
        #(judging by the fact we haven't returned from this function yet)
        #So let's just re-raise the last IOError we got
        raise e

    def data_to_temp(self, data):
        temp = (data*0.02) - 273.15
        return temp

    def get_amb_temp(self):
        data = self.read_reg(self.MLX90614_TA)
        return self.data_to_temp(data)

    def get_obj_temp(self):
        data = self.read_reg(self.MLX90614_TOBJ1)
        return self.data_to_temp(data)

    def get_human_temp(self):
        temp = self.get_obj_temp()
        temp = -0.000125*(temp**6)+0.0283429488*(temp**5)-2.67004808*(temp**4)+133.762569*(temp**3)-3758.41829*(temp**2)+56155.4892*temp-348548.755+temp
        start = time.clock()
        while temp < 35 or temp > 40: 
            if (time.clock() - start) > 10000:
                return -1
            temp = self.get_obj_temp()
            temp = -0.000125*(temp**6)+0.0283429488*(temp**5)-2.67004808*(temp**4)+133.762569*(temp**3)-3758.41829*(temp**2)+56155.4892*temp-348548.755+temp
        return temp

if __name__ == "__main__":
    sensor = MLX90614()
    print('amb temp:')
    print(sensor.get_amb_temp())
    print('obj temp:')
    print(sensor.get_obj_temp())
    print('human temp:')
    print(sensor.get_human_temp())