import time


fish = [3,4,3,1,2]
print(f'Initial: {fish}')
for day in range(1, 81):
    for i in range(len(fish)):
        # Beginning of day
        fish[i] -= 1
        if fish[i] < 0:
            fish[i] = 6
            fish.append(8)
    # End of day
    print(f'{len(fish):8} : {day:2} days: {fish}')
    time.sleep(0.1)
