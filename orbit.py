import os

os.environ['GALPY_NO_C'] = 'true' 

import numpy as np
import matplotlib.pyplot as plt
from galpy.orbit import Orbit
from galpy.potential import MWPotential2014
from astropy import units as u


os = Orbit(
    [8.122*u.kpc, -11.1*u.km/u.s, 239.1*u.km/u.s, 0.0208*u.kpc, 7.25*u.km/u.s, 0.*u.deg],
    ro=8.122, 
    vo=235.
)


ts = np.linspace(0., 0.25, 1000) * u.Gyr
os.integrate(ts, MWPotential2014)
fig = plt.figure(figsize=(12, 5))


plt.subplot(1, 2, 1)
os.plot(d1='x', d2='y', color='gold') 
plt.title("Top-Down View (Galactic Center at 0,0)")
plt.subplot(1, 2, 2)
os.plot(d1='R', d2='z', color='orange')
plt.title("Side View (Vertical Oscillation)")

plt.tight_layout()
plt.show()
