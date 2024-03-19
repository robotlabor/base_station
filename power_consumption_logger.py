import time
import os
import board
from adafruit_ina219 import INA219


i2c_bus = board.I2C()
ina219 = INA219(i2c_bus)

script_directory = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_directory, 'power_consumption_log.txt')

with open(log_file_path, 'a') as log_file:
    for _ in range(1800):
        bus_voltage = ina219.bus_voltage
        shunt_voltage = ina219.shunt_voltage
        current = ina219.current
        power = ina219.power

        total_voltage = bus_voltage + shunt_voltage

        power_consumption = bus_voltage * (current / 1000)

        current_charge = current / 1000  # Convert current from mA to A

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        log_data = f"{timestamp}, {total_voltage:.3f} V, {bus_voltage:.3f} V, {shunt_voltage:.5f} V, {current/1000:.4f} A, {power_consumption:.5f} W, {power:.3f} W\n"
        log_file.write(log_data)

        console_data = f"{timestamp}: Voltage (VIN+): {total_voltage:.3f} V, Voltage (VIN-): {bus_voltage:.3f} V, Shunt Voltage: {shunt_voltage:.5f} V, Shunt Current: {current/1000:.4f} A, Power Calc.: {power_consumption:.5f} W, Power Register: {power:.3f} W\n"
        print(console_data)

        if ina219.overflow:
            log_file.write("Internal Math Overflow Detected!\n")
            print("Internal Math Overflow Detected!")

        time.sleep(1)

