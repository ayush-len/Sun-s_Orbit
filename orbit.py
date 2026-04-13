import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


G = 6.67430e-11
M_p = 1.898e27    
m_s = 7.342e22    
R_s = 1.737e6     
a = 4.217e8       
k2 = 0.3         
Q = 100           


n = np.sqrt(G * M_p / a**3)      
I = (2/5) * m_s * R_s**2        
omega_0 = 3 * n                  
K = (3/2) * (k2 * G * M_p**2 * R_s**5) / (Q * a**6)


dt = 3.154e7 * 1e5              
total_years = 1e9               
steps = int(total_years * 3.154e7 / dt)


time_evolution = []
current_omega = omega_0
time_seconds = 0

for _ in range(steps):
    torque = -K * np.sign(current_omega - n)
    alpha = torque / I
    
    
    if (current_omega > n and current_omega + alpha * dt < n) or \
       (current_omega < n and current_omega + alpha * dt > n):
        current_omega = n
    else:
        current_omega += alpha * dt
    if abs(current_omega - n) < 1e-15: 
        current_omega = n
        torque = 0
    else:
        torque = -K * np.sign(current_omega - n)
    
    alpha = torque / I           
    current_omega += alpha * dt
    time_seconds += dt
    
    time_evolution.append({'Time_Years': time_seconds / 3.154e7, 
                           'Angular_Velocity': current_omega})


df = pd.DataFrame(time_evolution)

lock_row = df[df['Angular_Velocity'] == n].iloc[0] if n in df['Angular_Velocity'].values else None
lock_time = lock_row['Time_Years'] if lock_row is not None else "Not reached"


if isinstance(lock_time, (int, float)):
    print(f"Time to tidal locking: {lock_time:.2e} years")
else:
    print(f"Time to tidal locking: {lock_time}")


plt.figure(figsize=(10, 6))
plt.plot(df['Time_Years'], df['Angular_Velocity'], label='Satellite ω', color='cyan', linewidth=2)
plt.axhline(y=n, color='red', linestyle='--', label='Orbital Mean Motion (n)')
plt.title("Evolution of Satellite Angular Velocity under Tidal Torque")
plt.xlabel("Time (Years)")
plt.ylabel("Angular Velocity (rad/s)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
