import numpy as np
import matplotlib.pyplot as plt

data = [1, 2, 3, 4, 5, 3, 2 ,1]
bins = [0, 1, 2, 3, 4, 5, 6, 7]
plt.hist(data, bins = 100)
plt.show()