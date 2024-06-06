import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('SimulationData.csv', usecols=['Temperature', 'Time'], sep=',')

time_change = pd.to_datetime(data['Time'])
temperature_change = data['Temperature']

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(time_change, temperature_change, color='b', linestyle='-', linewidth=2, marker='.', label='Temperature')

ax.set_xlabel('Time', labelpad=10, fontsize=14)
ax.set_ylabel('Temperature (C°)', labelpad=25, fontsize=14)
ax.set_title('Temperature change over time', fontsize=18)

ax.tick_params(axis='x', labelrotation=45)
ax.tick_params(axis='both', labelsize=8)

num_ticks = 70
x_ticks = np.linspace(time_change.iloc[0], time_change.iloc[-1], num_ticks)
ax.set_xticks(x_ticks)

ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M:%S'))

ax.grid(True)
ax.legend(loc='upper left')

saved_path = 'AirConditioner_report.png'
plt.tight_layout()
plt.savefig(saved_path)
print("Plot saved:", saved_path)

plt.show()
