#bme280_data

def bme280data(sea_level_pressure, port):
    import smbus2
    import bme280

    address = 0x76
    bus = smbus2.SMBus(port)

    calibration_params = bme280.load_calibration_params(bus, address)

    # the sample method will take a single reading and return a
    # compensated_reading object
    bme280_data = bme280.sample(bus, address, calibration_params)

    # the compensated_reading class has the following attributes
    #print(data.id)
    #print(data.timestamp)
    #print(bme280_data.temperature)
    #print(bme280_data.pressure)
    #print(bme280_data.humidity)
    
    
    temperature = bme280_data.temperature-2
    pressure = bme280_data.pressure
    
    altitude = ((((sea_level_pressure/pressure)**(1/5.257))-1)*(temperature+273.15))/0.0065
    
    return [round(altitude), round(temperature)]

def bme280data_triple(sea_level_pressure):

    data_1 = bme280data(sea_level_pressure, 1)
    data_2 = bme280data(sea_level_pressure, 3)
    data_3 = bme280data(sea_level_pressure, 4)
    
    altitude = (data_1[0]+data_2[0]+data_3[0])/3
    temperature = (data_1[1]+data_2[1]+data_3[1])/3
    return [round(altitude), round(temperature)]

if __name__ == "__main__":
    
    values_1 = bme280data(1018.25, 1)
    values_2 = bme280data(1018.25, 3)
    values_3 = bme280data(1018.25, 4)
    #values_4 = bme280data_triple(1018.25)
    print(values_1)
    print(values_2)
    print(values_3)
    print("")
    #print(values_4)