def process_data(data):
    total = 0
    for i in range(len(data)):
        if data[i] < 0:
            continue
        for j in range(data[i]):
            if j % 2 == 0:
                total += j
    return total
