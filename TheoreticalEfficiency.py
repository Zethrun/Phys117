import numpy as np

def accuracy(probabilities):
    sum = 0
    for a in [probabilities[0], 1 - probabilities[0]]:
        for b in [probabilities[1], 1 - probabilities[1]]:
            for c in [probabilities[2], 1 - probabilities[2]]:
                for d in [probabilities[3], 1 - probabilities[3]]:
                    for e in [probabilities[4], 1 - probabilities[4]]:
                        det = [0 for p in [a, b, c, d, e] if p in probabilities]
                        if len(det) >= 3:
                            sum += a * b * c * d * e

    print(sum)
    

probabilities = [0.749, 0.679, 0.542, 0.985, 0.765]
accuracy(probabilities)

probabilities = [0.743, 0.677, 0.545, 0.986, 0.781]
accuracy(probabilities)

probabilities = [0.732, 0.673, 0.545, 0.984, 0.798]
accuracy(probabilities)
