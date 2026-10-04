import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np

# 1. Setup and load the 2025 Abu Dhabi Grand Prix
fastf1.plotting.setup_mpl(misc_mpl_mods=False)
session = fastf1.get_session(2025, 'Abu Dhabi', 'R')
session.load()

# 2. Target the podium finishers 
drivers = ['VER', 'NOR', 'PIA']
colors = ['#0600ef', '#ff8700', '#ff8000'] # Red Bull and McLaren colors

fig, ax = plt.subplots(figsize=(10, 6))

for driver, color in zip(drivers, colors):
    laps = session.laps.pick_driver(driver)
    
    # 3. Isolate the final stint of the race
    last_stint = laps['Stint'].max()
    stint_laps = laps[(laps['Stint'] == last_stint) & (laps['LapTime'].notnull())]
    
    # Remove in-laps, out-laps, or safety car laps to get clean racing data
    stint_laps = stint_laps.pick_quicklaps()
    
    x = stint_laps['LapNumber']
    y = stint_laps['LapTime'].dt.total_seconds()
    
    # Scatter plot the raw lap times
    ax.plot(x, y, marker='o', linestyle='none', color=color, alpha=0.4)
    
    # 4. Diagnostic Analytics: Calculate the Tire Degradation Slope
    if len(x) > 1:
        # np.polyfit calculates the linear trendline (1st degree polynomial)
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        
        # z[0] is the mathematical slope: exactly how much time is lost per lap
        deg_rate = z[0]
        
        # Plot the trendline
        ax.plot(x, p(x), color=color, linewidth=2, label=f'{driver} Deg: +{deg_rate:.3f}s/lap')

# 5. Format for the portfolio
ax.set_title("The Decider: Final Stint Tire Degradation (Abu Dhabi 2025)", fontsize=14, fontweight='bold')
ax.set_xlabel("Lap Number", fontsize=12, fontweight='bold')
ax.set_ylabel("Lap Time (Seconds)", fontsize=12, fontweight='bold')
ax.legend(loc='upper left')
ax.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
