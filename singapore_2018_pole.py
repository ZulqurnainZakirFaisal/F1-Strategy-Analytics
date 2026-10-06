import fastf1
import fastf1.plotting
import fastf1.utils
import matplotlib.pyplot as plt

fastf1.set_log_level('ERROR')
fastf1.plotting.setup_mpl(misc_mpl_mods=False)

session = fastf1.get_session(2018, 'Singapore', 'Q')
session.load()

# Top 6 from the Q3 results: (code, colour, line style)
drivers = [
    ('HAM', '#00d2be', '-'),   # Mercedes
    ('VER', '#1e41ff', '-'),   # Red Bull
    ('VET', '#dc0000', '-'),   # Ferrari
    ('BOT', '#00d2be', '--'),  # Mercedes
    ('RAI', '#dc0000', '--'),  # Ferrari
    ('RIC', '#1e41ff', '--'),  # Red Bull
]

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), sharex=True,
                                    gridspec_kw={'height_ratios': [3, 1, 1.5]})

# Hamilton's pole lap is the reference for the delta
ref_lap = session.laps.pick_drivers('HAM').pick_fastest()

for code, color, style in drivers:
    lap = session.laps.pick_drivers(code).pick_fastest()
    tel = lap.get_car_data().add_distance()
    time_str = str(lap['LapTime'])[-11:-3]  # e.g. 0:01:36.015 -> 1:36.015

    ax1.plot(tel['Distance'], tel['Speed'], color=color, linestyle=style,
             linewidth=1.5, label=f"{code} {time_str}")
    ax2.plot(tel['Distance'], tel['Throttle'], color=color, linestyle=style,
             linewidth=1.5)

    # Delta vs Hamilton (skip Hamilton himself)
    if code != 'HAM':
        delta, ref_tel, _ = fastf1.utils.delta_time(ref_lap, lap)
        ax3.plot(ref_tel['Distance'], delta, color=color, linestyle=style,
                 linewidth=1.5, label=code)

ax1.set_title("Top 6 Q3 Telemetry: Marina Bay (Singapore 2018)", fontsize=14, fontweight='bold')
ax1.set_ylabel('Speed (km/h)', fontsize=12, fontweight='bold')
ax1.legend(loc='lower right')
ax1.grid(True, linestyle='--', alpha=0.6)

ax2.set_ylabel('Throttle (%)', fontsize=12, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.6)

ax3.axhline(0, color='#00d2be', linewidth=2, label='HAM (reference)')
ax3.set_ylabel('Gap to HAM (s)', fontsize=12, fontweight='bold')
ax3.set_xlabel('Distance Covered on Track (meters)', fontsize=12, fontweight='bold')
ax3.legend(loc='upper left')
ax3.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('singapore_2018_telemetry_delta.png', dpi=150)
plt.show()