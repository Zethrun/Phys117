import numpy as np



a = [np.nan for i in range(4)]
a = [pog for pog in a if not np.isnan(pog)]

print(a)