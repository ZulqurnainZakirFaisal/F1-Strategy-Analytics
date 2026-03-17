!pip install fastf1
import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt

# 1. Keep the terminal clean
fastf1.set_log_level('ERROR')
fastf1.plotting.setup_mpl(misc_mpl_mods=False)

# 2. Load the 2021 Turkish Grand Prix Race
session = fastf1.get_session(2021, 'Turkey', 'R')
session.load()

# 3. Target Ocon (0 stops) and Bottas (Race Winner, 1 stop)
laps_oco = session.laps.pick_driver('OCO')
laps_bot = session.laps.pick_driver('BOT')

# 4. Initialize the Graph
fig, ax = plt.subplots(figsize=(10, 6))

# 5. Plot the lap times (Converting lap time to total seconds to plot it)
ax.plot(laps_oco['LapNumber'], laps_oco['LapTime'].dt.total_seconds(), color='#0090ff', label='Ocon (Zero Pit Stops)')
ax.plot(laps_bot['LapNumber'], laps_bot['LapTime'].dt.total_seconds(), color='#00d2be', label='Bottas (Standard Strategy)')

# 6. Make it look like a professional data report
ax.set_xlabel('Lap Number', fontsize=12, fontweight='bold')
ax.set_ylabel('Lap Time (Seconds)', fontsize=12, fontweight='bold')
ax.set_title("The Pirelli Cliff: Ocon's 57-Lap Intermediates Gamble (Turkey 2021)", fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.6)

# 7. Invert the Y-axis (In racing, a lower time is faster)
ax.invert_yaxis()

# Show the graph!
plt.show()
