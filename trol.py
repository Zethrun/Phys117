import numpy as np
planck = 6.626 * (10 ** -34)
boltz = 1.38 * (10 ** -23)
avogadros = 6 * (10 ** 23)
volume = 22.4/1000
mass = 14/(1000 * avogadros)
temp = 273 + 25
energy = (3 * boltz * temp) / 2

states = ((4 * np.pi * volume)/(3 * (planck ** 3))) * ((2 * mass * energy) ** (1 / 2)) * (2 * mass)
print(states)