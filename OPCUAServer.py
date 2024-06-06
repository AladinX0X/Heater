import os
import time
import socket
import opcua
import pandas as pd

current_dir = os.getcwd()
file_path = os.path.join(current_dir, "SimulationData_read.csv")

try:
    with open(file_path) as f:
        print("File exists:", file_path)
except FileNotFoundError:
    print("File does not exist:", file_path)
    exit()

df = pd.read_csv(file_path, sep=',', decimal='.', header=0, names=['Temperature', 'Status', 'Date', 'Time', 'DoorOpen'])
server = opcua.Server()
ip_address = socket.gethostbyname(socket.gethostname())
url = "opc.tcp://{}:8081".format(ip_address)
server.set_endpoint(url)
ns = server.register_namespace("Simulation")
objects = server.get_objects_node()
myobj = objects.add_object(ns, "Myobject")
temperature_var = myobj.add_variable(ns, "Temperature", 0.0)
status_var = myobj.add_variable(ns, "Status", "")
date_var = myobj.add_variable(ns, "Date", "")
time_var = myobj.add_variable(ns, "Time", "")
door_open_var = myobj.add_variable(ns, "DoorOpen", "")

server.start()

def update_opcua_variables():
    try:
        df_read = pd.read_csv(file_path, sep=',', decimal='.', header=0, names=['Temperature', 'Status', 'Date', 'Time', 'DoorOpen'])
        if not df_read.empty:
            temp_read = df_read.iloc[0]['Temperature']
            status_read = df_read.iloc[0]['Status']
            date_read = df_read.iloc[0]['Date']
            time_read = df_read.iloc[0]['Time']
            door_open_read = df_read.iloc[0]['DoorOpen']
            temperature_var.set_value(temp_read)
            status_var.set_value(status_read)
            date_var.set_value(date_read)
            time_var.set_value(time_read)
            door_open_var.set_value(door_open_read)
    except pd.errors.EmptyDataError:
        pass
    except FileNotFoundError:
        pass
try:
    while True:
        update_opcua_variables()
        time.sleep(1)
finally:
    server.stop()
