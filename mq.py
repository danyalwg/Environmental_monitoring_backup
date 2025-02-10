from machine import ADC, Pin
from time import sleep

# Pin configuration
mq9_analog = ADC(Pin(35))        # MQ-9 Analog pin connected to GPIO35
mq9_analog.atten(ADC.ATTN_11DB)  # Configure ADC for full-scale 3.3V
mq9_analog.width(ADC.WIDTH_12BIT)  # 12-bit resolution (0-4095)

mq135_analog = ADC(Pin(32))      # MQ-135 Analog pin connected to GPIO32
mq135_analog.atten(ADC.ATTN_11DB)
mq135_analog.width(ADC.WIDTH_12BIT)

# Calibration values (adjust after calibration in clean air)
R0_MQ9 = 0.49    # R0 value for MQ-9
R0_MQ135 = 5.29  # R0 value for MQ-135

# Function to map a value
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Function to calculate gas concentrations for MQ-9
def calculate_concentration_mq9(ratio, gas):
    if gas == "LPG":
        if ratio > 1.8:
            return 200
        elif ratio > 1.0:
            return 1000
        elif ratio > 0.6:
            return 5000
        else:
            return 10000
    elif gas == "CO":
        if ratio > 2.2:
            return 100
        elif ratio > 1.2:
            return 200
        elif ratio > 0.8:
            return 400
        else:
            return 1000
    elif gas == "CH4":
        if ratio > 1.7:
            return 200
        elif ratio > 1.0:
            return 500
        elif ratio > 0.7:
            return 1000
        else:
            return 5000
    return 0

# Function to calculate gas concentrations for MQ-135
def calculate_concentration_mq135(ratio, gas):
    if gas == "CO2":
        if ratio > 3.5:
            return 10
        elif ratio > 2.5:
            return 20
        elif ratio > 1.5:
            return 100
        elif ratio > 1.0:
            return 200
        else:
            return 500
    elif gas == "CO":
        if ratio > 2.5:
            return 10
        elif ratio > 1.8:
            return 20
        elif ratio > 1.2:
            return 100
        elif ratio > 0.8:
            return 200
        else:
            return 500
    elif gas == "NH4":
        if ratio > 2.2:
            return 10
        elif ratio > 1.5:
            return 50
        elif ratio > 1.0:
            return 100
        else:
            return 200
    return 0

# Function to read sensors and calculate concentrations
def read_sensors():
    # MQ-9 Analog Reading
    sensor_value_mq9 = mq9_analog.read()
    sensor_voltage_mq9 = (sensor_value_mq9 / 4095.0) * 3.3
    if sensor_voltage_mq9 > 0:
        rs_gas_mq9 = (3.3 - sensor_voltage_mq9) / sensor_voltage_mq9
        ratio_mq9 = rs_gas_mq9 / R0_MQ9
    else:
        rs_gas_mq9 = 0
        ratio_mq9 = 0

    # MQ-135 Analog Reading
    sensor_value_mq135 = mq135_analog.read()
    sensor_voltage_mq135 = (sensor_value_mq135 / 4095.0) * 3.3
    if sensor_voltage_mq135 > 0:
        rs_gas_mq135 = (3.3 - sensor_voltage_mq135) / sensor_voltage_mq135
        ratio_mq135 = rs_gas_mq135 / R0_MQ135
    else:
        rs_gas_mq135 = 0
        ratio_mq135 = 0

    # Calculate MQ-9 concentrations
    concentration_lpg = calculate_concentration_mq9(ratio_mq9, "LPG")
    concentration_co_mq9 = calculate_concentration_mq9(ratio_mq9, "CO")
    concentration_ch4 = calculate_concentration_mq9(ratio_mq9, "CH4")

    # Calculate MQ-135 concentrations
    if ratio_mq135 > 0:
        concentration_co2 = calculate_concentration_mq135(ratio_mq135, "CO2")
        concentration_co_mq135 = calculate_concentration_mq135(ratio_mq135, "CO")
        concentration_nh4 = calculate_concentration_mq135(ratio_mq135, "NH4")
    else:
        concentration_co2 = 0
        concentration_co_mq135 = 0
        concentration_nh4 = 0

    # Return all results as a dictionary
    return {
        "MQ-9": {
            "Raw_ADC": sensor_value_mq9,
            "Voltage": sensor_voltage_mq9,
            "Rs/R0": ratio_mq9,
            "LPG": concentration_lpg,
            "CO": concentration_co_mq9,
            "CH4": concentration_ch4
        },
        "MQ-135": {
            "Raw_ADC": sensor_value_mq135,
            "Voltage": sensor_voltage_mq135,
            "Rs/R0": ratio_mq135,
            "CO2": concentration_co2,
            "CO": concentration_co_mq135,
            "NH4": concentration_nh4
        }
    }

# Main loop
if __name__ == "__main__":
    while True:
        data = read_sensors()
        print("MQ-9 Data:", data["MQ-9"])
        print("MQ-135 Data:", data["MQ-135"])
        sleep(1)
