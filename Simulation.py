import pandas as pd
import time
from time import sleep
import threading as thr
import numpy as np
import datetime as dt
import os
import json
#---------------------------------------------------------------------------------------------

path_data_read = os.path.join(os.path.curdir, 'SimulationData_read.csv')
path_data = os.path.join(os.path.curdir, 'SimulationData.csv')

df = pd.DataFrame(columns=['Temperature', 'Status', 'Fan', 'Date', 'Time', 'Door Status'])

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
        self.fan_status = 'ON' if use_fan else 'OFF'
        self.door_open = False
        self.result_list = []

    def run(self):
        print(f"Air Conditioner starting at: {dt.datetime.now().strftime('%H:%M:%S')}")
        self.date_time = time.time()
        self.simulation_process()

    def simulation_process(self):
        hysteresis = 0.5
        off_time = 10
        
        try:
            while True:
                time_form = dt.datetime.now().strftime('%H:%M:%S')
                date_form = dt.datetime.now().strftime('%Y-%m-%d')
                printed_temp = str(self.temperature)[:str(self.temperature).find('.') + 2]
                
                # External factors
                external_temp = np.random.uniform(15, 30)
                time_of_day = dt.datetime.now().hour
                
                # Simulate a gradual drift over time
                drift = np.sin(time.time() / 3600) * 0.05  # Small drift over time
                
                # Adjust temperature based on target and external factors
                if self.status == 'ON':
                    if self.temperature < self.target_temp + hysteresis:
                        self.temperature += np.random.normal(0.15, 0.05)  # Random normal increase
                    else:
                        self.status = 'OFF'
                        sleep(off_time)
                elif self.status == 'OFF':
                    if self.temperature > self.target_temp - hysteresis:
                        self.temperature -= np.random.normal(0.15, 0.05)  # Random normal decrease
                    else:
                        self.status = 'ON'

                # Apply external factors
                if self.door_open:
                    self.temperature += np.random.normal(0.3, 0.1)  # More rapid increase if door is open
                else:
                    self.temperature += (external_temp - self.temperature) * 0.01  # Gradual adjustment towards external temp
                
                # Apply drift
                self.temperature += drift
                
                # Simulate door status change periodically
                self.simulate_random_door_status()
            
                self.record_data(time_form, date_form, printed_temp)
            
                self.result_list.append([printed_temp, self.status, self.fan_status, date_form, time_form])
                sleep(1)

                if self.auto_timer is not None and time.time() - self.date_time >= self.auto_timer:
                    break

        finally:
            self.finalize_simulation()

    def simulate_random_door_status(self):
        # Randomly change door status with a small probability
        if not self.door_open and np.random.rand() < 0.05:  # 5% chance to open the door every second
            self.door_open = True
            door_open_duration = np.random.uniform(5, 8)
            for _ in range(int(door_open_duration)):
                self.adjust_temperature_due_to_door()
                sleep(1)
            self.door_open = False

    def adjust_temperature_due_to_door(self):
        if self.door_open:
            self.temperature += np.random.uniform(0.5, 1)  # Incremental temperature increase if door is opened
        else:
            self.temperature -= np.random.uniform(0.1, 0.3)  # Incremental temperature decrease when door is closed
        self.record_data(dt.datetime.now().strftime('%H:%M:%S'), dt.datetime.now().strftime('%Y-%m-%d'), str(self.temperature)[:str(self.temperature).find('.') + 2])

    def record_data(self, time_form, date_form, printed_temp):
        door_status = 'Open' if self.door_open else 'Closed'
        read_list = {
            'Temperature': [printed_temp],
            'Status': [self.status],
            'Fan': [self.fan_status],
            'Date': [date_form],
            'Time': [time_form],
            'Door Status': [door_status]
        }
        data = pd.DataFrame(read_list, columns=['Temperature', 'Status', 'Fan', 'Date', 'Time', 'Door Status'])
        data.to_csv(path_data_read, mode='a', header=False, index=False)  # Append without header
        self.generate_data_json()  # Add this line to generate data.json

    def generate_data_json(self):
        df = pd.read_csv(path_data_read)
        if df.empty:
            print("No data available to write to data.json")
            return
        latest_data = df.iloc[-1].to_dict()  # Get the latest row
        with open('frontend/data.json', 'w') as json_file:
            json.dump(latest_data, json_file)

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
