import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Physical Constants
G = 6.67430e-11
M_p = 1.898e27    # Mass of Jupiter (kg)
m_s = 7.342e22    # Mass of Moon (kg)
R_s = 1.737e6     # Radius of Moon (m)
a = 4.217e8       # Semi-major axis (m)
k2 = 0.3          # Love number (typical for rocky bodies)
Q = 100           # Quality factor (typical for rocky bodies)

# 2. Calculated Quantities
n = np.sqrt(G * M_p / a**3)      # Orbital mean motion (target angular velocity)
I = (2/5) * m_s * R_s**2         # Moment of Inertia
omega_0 = 3 * n                  # Initial rotation (spinning 3x faster than orbit)

# 3. Torque Constant (Grouping constant terms)
# Torque = -K * sgn(omega - n)
K = (3/2) * (k2 * G * M_p**2 * R_s**5) / (Q * a**6)

# 4. Simulation Parameters
dt = 3.154e7 * 1e5               # 100,000 years per step
total_years = 1e9                # 1 billion year simulation
steps = int(total_years * 3.154e7 / dt)

# 5. Integration Loop
time_evolution = []
current_omega = omega_0
time_seconds = 0

for _ in range(steps):
    torque = -K * np.sign(current_omega - n)
    alpha = torque / I
    
    # If the next step would cross the 'n' threshold, just set it to 'n'
    if (current_omega > n and current_omega + alpha * dt < n) or \
       (current_omega < n and current_omega + alpha * dt > n):
        current_omega = n
    else:
        current_omega += alpha * dt
    if abs(current_omega - n) < 1e-15: # Check for locking
        current_omega = n
        torque = 0
    else:
        torque = -K * np.sign(current_omega - n)
    
    alpha = torque / I           # Angular acceleration
    current_omega += alpha * dt
    time_seconds += dt
    
    time_evolution.append({'Time_Years': time_seconds / 3.154e7, 
                           'Angular_Velocity': current_omega})

# 6. Data Storage with Pandas
df = pd.DataFrame(time_evolution)

# 7. Determine Time to Tidal Locking
lock_row = df[df['Angular_Velocity'] == n].iloc[0] if n in df['Angular_Velocity'].values else None
lock_time = lock_row['Time_Years'] if lock_row is not None else "Not reached"

# Check if it's a number (float/int) before trying to format it
if isinstance(lock_time, (int, float)):
    print(f"Time to tidal locking: {lock_time:.2e} years")
else:
    print(f"Time to tidal locking: {lock_time}")

# 8. Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['Time_Years'], df['Angular_Velocity'], label='Satellite ω', color='cyan', linewidth=2)
plt.axhline(y=n, color='red', linestyle='--', label='Orbital Mean Motion (n)')
plt.title("Evolution of Satellite Angular Velocity under Tidal Torque")
plt.xlabel("Time (Years)")
plt.ylabel("Angular Velocity (rad/s)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
