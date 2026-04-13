import os
# FIX: Tell galpy to skip the C-extension and avoid the DLL error
os.environ['GALPY_NO_C'] = 'true' 

import numpy as np
import matplotlib.pyplot as plt
from galpy.orbit import Orbit
from galpy.potential import MWPotential2014
from astropy import units as u

# 1. Initialize the Sun's orbit
# Coordinates: R, vR, vT, z, vz, phi
# Use u.s (seconds) so Python knows it's a unit, not a variable
os = Orbit(
    [8.122*u.kpc, -11.1*u.km/u.s, 239.1*u.km/u.s, 0.0208*u.kpc, 7.25*u.km/u.s, 0.*u.deg],
    ro=8.122, 
    vo=235.
)

# 2. Define the time array (250 million years)
ts = np.linspace(0., 0.25, 1000) * u.Gyr

# 3. Integrate the orbit in the MWPotential2014
os.integrate(ts, MWPotential2014)

# --- Visualization ---
fig = plt.figure(figsize=(12, 5))

# Plot 1: Top-down view (X vs Y)
# REMOVED overplot=True so it auto-scales to ~8kpc
plt.subplot(1, 2, 1)
os.plot(d1='x', d2='y', color='gold') 
plt.title("Top-Down View (Galactic Center at 0,0)")

# Plot 2: Side view (R vs Z)
# REMOVED overplot=True
plt.subplot(1, 2, 2)
os.plot(d1='R', d2='z', color='orange')
plt.title("Side View (Vertical Oscillation)")

plt.tight_layout()
plt.show()
