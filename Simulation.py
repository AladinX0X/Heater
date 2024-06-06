import pandas as pd
import time
from time import sleep
import threading as thr
import numpy as np
import datetime as dt
import sys
import os
#---------------------------------------------------------------------------------------------

path_data_read = os.path.join(os.path.curdir, 'SimulationData_read.csv')
path_data = os.path.join(os.path.curdir, 'SimulationData.csv')

df = pd.DataFrame(columns=['Temperature', 'Status', 'Fan', 'Date', 'Time', 'DoorOpen'])

if os.path.isfile(path_data_read):
    df.to_csv(path_data_read, mode='a', header=True, index=False)  
else:
    df.to_csv(path_data_read, mode='w', header=True, index=False)  

if os.path.isfile(path_data):
    df.to_csv(path_data, mode='a', header=True, index=False)  
else:
    df.to_csv(path_data, mode='w', header=True, index=False)

class Simulation(thr.Thread):
    
    def __init__(self, target_temp, use_fan, auto_timer=900):
        thr.Thread.__init__(self)
        self.target_temp = target_temp
        self.use_fan = use_fan
        self.auto_timer = auto_timer
        self.temperature = np.random.uniform(20, 25)
        self.status = 'OFF'
        self.fan_status = 'OFF' if use_fan else 'OFF'
        self.door_open = False
        self.result_list = []

    def run(self):
        print(f"Air Conditioner starting at: {dt.datetime.now().strftime('%H:%M:%S')}")
        self.date_time = time.time()
        self.simulation_process()

    def simulation_process(self):
        try:
            while True:
                time_form = dt.datetime.now().strftime('%H:%M:%S')
                date_form = dt.datetime.now().strftime('%Y-%m-%d')
                printed_temp = str(self.temperature)[:str(self.temperature).find('.') + 2]
                
                if self.temperature < self.target_temp:
                    self.temperature += np.random.uniform(0.1, 0.3)
                elif self.temperature > self.target_temp:
                    self.temperature -= np.random.uniform(0.1, 0.3)
                
                if self.temperature == 25 and not self.door_open:
                    self.simulate_door_open()
                    continue

                if self.temperature != float(printed_temp) or self.status != self.status or self.fan_status != self.fan_status or self.door_open:
                    self.record_data(time_form, date_form, printed_temp)
                
                self.result_list.append([printed_temp, self.status, self.fan_status, date_form, time_form])
                sleep(1)

                if self.auto_timer is not None and time.time() - self.date_time >= self.auto_timer:
                    break

        finally:
            self.finalize_simulation()

    def simulate_door_open(self):
        print(f"Door or window opened at: {dt.datetime.now().strftime('%H:%M:%S')}")
        prev_temperature = self.temperature
        prev_status = self.status
        self.door_open = True
        self.temperature += np.random.uniform(3, 6)
        self.status = 'OFF'
        
        time_form = dt.datetime.now().strftime('%H:%M:%S')
        date_form = dt.datetime.now().strftime('%Y-%m-%d')
        printed_temp = str(self.temperature)[:str(self.temperature).find('.') + 2]
        self.record_data(time_form, date_form, printed_temp, door_open=True)
        
        sleep(15)
        
        self.temperature = prev_temperature
        self.status = prev_status
        self.door_open = False
        
        time_form = dt.datetime.now().strftime('%H:%M:%S')
        date_form = dt.datetime.now().strftime('%Y-%m-%d')
        printed_temp = str(self.temperature)[:str(self.temperature).find('.') + 2]
        self.record_data(time_form, date_form, printed_temp, door_open=False)

    def record_data(self, time_form, date_form, printed_temp, door_open=False):
        door_status = 'Open' if door_open else 'Closed'
        read_list = {
            'Temperature': [printed_temp],
            'Status': [self.status],
            'Fan': [self.fan_status],
            'Date': [date_form],
            'Time': [time_form],
            'Door Status': [door_status]
        }
        data = pd.DataFrame(read_list, columns=['Temperature', 'Status', 'Fan', 'Date', 'Time', 'Door Status'])
        data.to_csv(path_data_read, index=False)

    def finalize_simulation(self):
        self.fan_status = 'OFF'
        time_form = dt.datetime.now().strftime('%H:%M:%S')
        date_form = dt.datetime.now().strftime('%Y-%m-%d')
        printed_temp = str(self.temperature)[:str(self.temperature).find('.') + 2]
        self.record_data(time_form, date_form, printed_temp)
        
        data = pd.DataFrame(self.result_list, columns=['Temperature', 'Status', 'Fan', 'Date', 'Time'])
        data.to_csv(path_data, index=False)
        print(f"Simulation ended at: {dt.datetime.now().strftime('%H:%M:%S')}, Final Temperature: {self.temperature:.2f}")

if __name__ == '__main__':
    try:
        target_temp = float(input('Enter the wished room Temperature (in °C): '))

        use_fan_input = input('Turn on the fan? (yes/no): ').lower()
        use_fan = use_fan_input == 'yes' if use_fan_input else False

        simulation = Simulation(target_temp, use_fan)
        simulation.start()

        while simulation.is_alive():
            door_status = 'Open' if simulation.door_open else 'Closed'
            print(f"Time: {dt.datetime.now().strftime('%H:%M:%S')}, Status: {simulation.status}, Fan: {simulation.fan_status}, Temperature: {simulation.temperature:.2f}, Door Status: {door_status}")
            sleep(1)

    except KeyboardInterrupt:
        print("\nAir Conditioner stopped...")
        simulation.join()
