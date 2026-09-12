import math

minute_list = []
hours = []

for adding_factor in range(180, 511, 30):
    i = 0
    step = 1

    while True:
        result = (i + adding_factor) / 12

        if result > i:
            i += step
        else:
            i -= step
            step /= 10

        if abs(i - result) < 0.0000001:
            break

    minutes = (adding_factor + i) / 6
    hour = (adding_factor - 180) // 30

    if minutes > 61: # Trust me, 60 doesn't work
        hour += 1
        minutes %= 60


    minute_list.append(minutes)
    seconds = 60 * (minutes - math.floor(minutes))

    # Construct string
    hour_str = ""
    hour_str += f"{hour}"
    if 60 < minutes < 61:
        hour_str += f":00"
    else:
        hour_str += f":{minutes:.0f}"

    hour_str += f":{seconds:.0f}"

    hours.append(hour_str)

diff = []
for i in range(len(minute_list) - 1):
    if minute_list[i] > minute_list[i + 1]:
        diff.append((minute_list[i + 1] + minute_list[i]) % 60)
    else:
        diff.append(minute_list[i + 1] - minute_list[i])

print(f"Hours:{hours}")
print(f"Raw minutes: {minute_list}")

raw_change = sum(diff) / len(diff)

minute_change = math.floor(raw_change)
second_change = (raw_change - minute_change) * 60

print(f"Average change per hour: {minute_change}m {second_change:.0f}s")
