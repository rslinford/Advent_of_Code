import time
from collections import defaultdict

with open('fish.txt', 'r') as f:
    text = f.read()
fish = [int(x) for x in text.split(',')]
fish_short = [3, 4, 3, 1, 2]

def naive_solution():
    print(f'Initial: {fish}')
    for day in range(1, 257):
        for i in range(len(fish)):
            # Beginning of day
            fish[i] -= 1
            if fish[i] < 0:
                fish[i] = 6
                fish.append(8)
        # End of day
        print(f'{len(fish):10} : {day:2} days: {fish[:100]}')
        # time.sleep(0.1)


def def_value():
    return 0

d = defaultdict(def_value)
#  1,740,449,478,328
#  1,639,854,996,917
#     26,984,457,539


#  Populate dictionary with data from file
for x in fish:
    d[x] += 1

for day in range(1, 257):
    print(f'Day {day}')
    zeros = d[0]
    d[0] = d[1]
    d[1] = d[2]
    d[2] = d[3]
    d[3] = d[4]
    d[4] = d[5]
    d[5] = d[6]
    d[6] = d[7]
    d[7] = d[8]
    d[6] += zeros
    d[8] = zeros
    score = 0
    for n in range(9):
        score += d[n]
        print(n, d[n])
    print(f'Score {score}')
    print()
    # time.sleep(1.5)
