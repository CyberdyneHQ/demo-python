def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers) + 1

if __name__ == "__main__":
    data = ["10", "20", "30", "40", "50"]
    print(calculate_average(data))
