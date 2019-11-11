#gy271_data
import py_qmc5883l
#import smbus
from cmath import rect, phase
from math import radians, degrees
import math

def mean_angle(deg):
    return degrees(phase(sum(rect(1, radians(d)) for d in deg)/len(deg)))

def gy271data():
    #sensor on board1
    sensor_1 = py_qmc5883l.QMC5883L(1)
    sensor_1.calibration = [[1.5780509280722965, 0.038105731303876844, 1504.1238679228964],
                            [0.03810573130387683, 1.0025119702913472, -1540.304996458992],
                            [0.0, 0.0, 1.0]]
    sensor_1.declination = 3
    compass_heading_1 = sensor_1.get_bearing()
    
    #sensor on board2
    sensor_2 = py_qmc5883l.QMC5883L(3)
    sensor_2.calibration = [[1.044079609156316, -0.015382668052023707, -63.0440117109887],
                            [-0.015382668052023707, 1.0053681618536958, -1530.097140668346],
                            [0.0, 0.0, 1.0]]
    sensor_2.declination = 3
    compass_heading_2 = sensor_2.get_bearing()
    
    #sensor on board3
    sensor_3 = py_qmc5883l.QMC5883L(4)
    sensor_3.calibration = [[1.5222818208476216, 0.08676788232810626, 996.2389626264803],
                            [0.0867678823281062, 1.0144149482198819, 2203.742176129511],
                            [0.0, 0.0, 1.0]]
    sensor_3.declination = 3
    compass_heading_3 = sensor_3.get_bearing()
    
    #mean_sinus = (math.sin(compass_heading_1)+math.sin(compass_heading_2)+math.sin(compass_heading_3))/3
    #mean_cosinus = (math.cos(compass_heading_1)+math.cos(compass_heading_2)+math.cos(compass_heading_3))/3
    #compass_heading = math.atan(mean_sinus/mean_cosinus)
    compass_heading = mean_angle([compass_heading_1, compass_heading_2, compass_heading_3])
    
    if __name__ == "__main__":
        print(compass_heading_1)
        print(compass_heading_2)
        print(compass_heading_3)
        print("")
        print(compass_heading)
        print("")
        print("")
        
    return round(compass_heading)

if __name__ == "__main__":
    while True:
        gy271data()