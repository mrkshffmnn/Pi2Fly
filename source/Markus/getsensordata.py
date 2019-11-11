#sensordata
#.py for getting all the sensor data in a nice format

from gy271_data import gy271data
from bme280_data import bme280data_triple
from mpu6050_data import mpu6050data
from mpxv7002dp_data import mpxv7002dpdata

def getsensordata():
    
    compass_heading = "no compass data"
    altitude = "no alitmeter data"
    temperature = "no thermal data"
    pitch = "no gyro data"
    roll = "no gyro data"
    airspeed = "no pitot data"
    
    try:compass_heading = gy271data()
    except Exception as e: print(e)
    try:[altitude, temperature] = bme280data_triple(1018.25)
    except Exception as e: print(e)
    try:[pitch, roll] = mpu6050data()
    except Exception as e:print(e)
    try:airspeed = mpxv7002dpdata()
    except Exception as e: pass#print(e)
    
    return [compass_heading, altitude, temperature, pitch, roll, airspeed]

if __name__ == "__main__":

    [compass_heading, altitude, temperature, pitch, roll, airspeed] = getsensordata()

    print("Heading Angle = ", compass_heading, "°")
    print("Temperature = ", temperature, "°C")
    print("Altitude = ", altitude, "m")
    print("Pitch = ", pitch, "°")
    print("Roll = ", roll, "°")
    print("Airspeed = ", airspeed, "m/s")
