import numpy as np



a = "(1, 2, 3, 4, 5)"
a = a.strip("()").split(", ")

print(a, type(a))

a = [int(el) for el in a]

print(a, type(a))

b = [int(el) for el in "(1, 2, 3, 4, 5)".strip("()").split(", ")]

print(b, type(b))