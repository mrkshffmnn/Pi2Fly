from getsensordata import getsensordata

while True:
    
    [compass_heading, altitude, temperature, pitch, roll, airspeed] = getsensordata()
    print("")
    print("----------")
    print("Heading Angle = ", compass_heading, "°")
    print("Temperature = ", temperature, "°C")
    print("Altitude = ", altitude, "m")
    print("Pitch = ", pitch, "°")
    print("Roll = ", roll, "°")
    print("Airspeed = ", airspeed, "m/s")
    