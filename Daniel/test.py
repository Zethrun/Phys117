import numpy as np

a = 0
binsize = 2
b = 11.5

print((b-a)/binsize)

b = a + round((b-a)/binsize)*binsize

print((b-a)/binsize)
print(np.linspace(a,b,num=(int((b-a)/binsize))-1))
