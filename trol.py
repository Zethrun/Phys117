import numpy as np
import matplotlib.pyplot as plt

ang = 0.001
speed = 0
time = 0
grav = 9.81

times = []
datas = [[], [], []]
ylabels = ["Angles [radians]" , "Speeds [radians/s]", "Acceleration "]
radius = 0.2

while True:
    if ang <= np.
    dt = 0.000001
    time += dt
    times.append(time)
    acceleration = grav * np.sin(ang) / radius
    datas[2].append(acceleration)
    dang = speed * dt
    ang += dang
    datas[0].append(ang)
    dspeed = acceleration * dt
    speed += dspeed
    datas[1].append(speed)
    if ang >= 3 * np.pi:
        break


fig = plt.figure()
style = "seaborn-darkgrid"
plt.style.use(style)
subfigs = fig.subfigures(1, len(datas))

for plot_index, subfig in enumerate(subfigs):
    ax = subfig.subplots(1)
    ylabel = ylabels[plot_index]
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Angle [radians]")
    data = datas[plot_index]
    ax.plot(datas[0], data)

plt.show()