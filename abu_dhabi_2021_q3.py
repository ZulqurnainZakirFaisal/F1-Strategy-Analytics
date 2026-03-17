import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt

# 1. Clean up the console
fastf1.set_log_level('ERROR')
fastf1.plotting.setup_mpl(misc_mpl_mods=False)

# 2. Load the 2021 Abu Dhabi Qualifying Session
session = fastf1.get_session(2021, 'Abu Dhabi', 'Q')
session.load()

# 3. Get the absolute fastest laps for Max and Lewis
lap_ver = session.laps.pick_driver('VER').pick_fastest()
lap_ham = session.laps.pick_driver('HAM').pick_fastest()

# 4. Extract the raw car telemetry (Speed, Throttle, Brakes, Distance)
tel_ver = lap_ver.get_car_data().add_distance()
tel_ham = lap_ham.get_car_data().add_distance()

# 5. Build a multi-panel graph (2 rows, 1 column)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [2, 1]})
fig.suptitle("The Title Decider: Verstappen vs Hamilton Telemetry (Abu Dhabi 2021 Q3)", fontsize=16, fontweight='bold')

# --- TOP PLOT: SPEED ---
ax1.plot(tel_ver['Distance'], tel_ver['Speed'], color='#0600ef', label='Verstappen (Pole)')
ax1.plot(tel_ham['Distance'], tel_ham['Speed'], color='#00d2be', label='Hamilton (P2)')
ax1.set_ylabel('Speed (km/h)', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.5)

# --- BOTTOM PLOT: THROTTLE PERCENTAGE ---
ax2.plot(tel_ver['Distance'], tel_ver['Throttle'], color='#0600ef')
ax2.plot(tel_ham['Distance'], tel_ham['Throttle'], color='#00d2be')
ax2.set_ylabel('Throttle (%)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Distance Covered on Track (meters)', fontsize=12, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.5)

# 6. Make it look perfectly spaced
plt.tight_layout()
plt.show()
