import argparse
import subprocess as sb
import webbrowser
import os
import time

parser = argparse.ArgumentParser(description='Simulate and visualize air conditioning system.')
parser.add_argument('target_temp', type=float, help='Enter the desired room temperature (in °C)')
parser.add_argument('use_fan', type=str, choices=['yes', 'no'], help='Turn on the fan? (yes/no)')
parser.add_argument('time_in_minutes', type=int, help='Enter time in minutes')

args = parser.parse_args()

target_temp = args.target_temp
use_fan = args.use_fan == 'yes'
time_in_minutes = args.time_in_minutes

opcua_proc = sb.Popen(['python', 'OPCUAServer.py'])

sim_proc = sb.Popen(['python', 'Simulation.py', str(target_temp), str(use_fan), str(time_in_minutes)])

time.sleep(2)

web_dir = os.path.join(os.path.dirname(__file__), 'frontend')
webserver_proc = sb.Popen(['python', 'Webserver.py'], cwd=web_dir)

webbrowser.open('http://localhost:8000/')

sim_proc.wait()

opcua_proc.terminate()
webserver_proc.terminate()

graphic_proc = sb.Popen(['python', 'Graphic.py'])
graphic_proc.wait()

print("All processes completed.")
