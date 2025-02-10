from mq import read_sensors
from uv import read_uv_sensor
from bme import read_bme280
from rtc import get_time
from dust_sensor import read_dust_sensor
from time import sleep

def format_time_12hr(hour, minute, second):
    """
    Converts 24-hour time to 12-hour format with AM/PM.
    """
    am_pm = 'AM'
    if hour >= 12:
        am_pm = 'PM'
        if hour > 12:
            hour -= 12
    if hour == 0:
        hour = 12  # Midnight edge case
    return f"{hour:02}:{minute:02}:{second:02} {am_pm}"

def main():
    while True:
        # Read RTC time dynamically
        rtc_time = get_time()
        formatted_time = format_time_12hr(rtc_time['hour'], rtc_time['minute'], rtc_time['second'])

        # Read MQ sensor data
        mq_data = read_sensors()

        # Read UV sensor data
        uv_data = read_uv_sensor()

        # Read BME280 sensor data
        bme_data = read_bme280()

        # Read Dust Sensor data
        dust_data = read_dust_sensor()

        # Display RTC time
        print("RTC Time:")
        print(f"  Date: {rtc_time['day']:02}-{rtc_time['month']:02}-{rtc_time['year']}")
        print(f"  Time: {formatted_time}")

        # Display MQ-9 sensor data
        print("\nMQ-9 Sensor Data:")
        print(f"  LPG: {mq_data['MQ-9']['LPG']} ppm")
        print(f"  CO: {mq_data['MQ-9']['CO']} ppm")
        print(f"  CH4: {mq_data['MQ-9']['CH4']} ppm")

        # Display MQ-135 sensor data
        print("\nMQ-135 Sensor Data:")
        print(f"  CO2: {mq_data['MQ-135']['CO2']} ppm")
        print(f"  NH4: {mq_data['MQ-135']['NH4']} ppm")

        # Display UV sensor data
        print("\nUV Sensor Data:")
        print(f"  Raw ADC: {uv_data['Raw_ADC']}")
        print(f"  UV Intensity: {uv_data['UV_Intensity']:.2f} mW/cm²")
        print(f"  UV Index: {uv_data['UV_Index']:.2f}")

        # Display BME280 sensor data
        print("\nBME280 Sensor Data:")
        print(f"  Temperature: {bme_data['Temperature']:.2f} °C")
        print(f"  Pressure: {bme_data['Pressure']:.2f} hPa")
        print(f"  Humidity: {bme_data['Humidity']:.2f} %")

        # Display Dust Sensor data
        print("\nDust Sensor Data:")
        print(f"  Dust Density: {dust_data['Dust_Density']:.2f} µg/m³")
        print(f"  AQI: {dust_data['AQI']}")
        print(f"  Health Level: {dust_data['Health_Level']}")

        # Separator
        print("-" * 50)

        # Delay for 1 second
        sleep(1)

if __name__ == "__main__":
    main()
