import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
factor = 1

planck = 6.626 * (10 ** -34)
boltz = 1.38 * (10 ** -23)
avogadros = 6 * (10 ** 23)
volume = (22.4/1000) / factor
side_length = np.cbrt(volume)
mass = 14/(1000 * avogadros) / factor
temp = 273 + 25
energy = ((3 * boltz * temp) / 2)

x, y = [], []

limit = int(np.floor(np.sqrt(energy / ((planck ** 2)/(8 * mass * (side_length ** 2))))))
interval = 10
print(limit)

factor = 10 ** 30

for nx in tqdm(range(limit - interval, limit)):
    ny_limit = int(np.floor(np.sqrt(limit ** 2 - nx ** 2)))
    for ny in range(ny_limit - interval, ny_limit):
        nz_limit = int(np.floor(np.sqrt(limit ** 2 - nx ** 2 - ny ** 2)))
        for nz in range(nz_limit - interval, nz_limit):
            sum_squares = nx**2 + ny**2 + nz**2
            state_energy = ((planck ** 2)/(8 * mass * (side_length ** 2))) * sum_squares * factor
            if state_energy <= energy * factor:
                print(state_energy)
                if state_energy not in x:
                    x.append(state_energy)
                y.append((nx, ny, nz))

print(len(x))
print(len(y))
print(len(y) / len(x))

# y_new = []
# combinations = 0
# for combination in y:
#     combinations += combination
#     y_new.append(combinations)

# style = "seaborn-darkgrid"
# plt.style.use(style)
# plt.plot(x, y_new)
# plt.show()