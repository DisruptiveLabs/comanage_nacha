def calculate_check_digit(routing_number):
    routing_number = str(routing_number)
    digits = [int(c) for c in routing_number]
    weights = [3, 7, 1, 3, 7, 1, 3, 7]

    assert len(digits) == len(weights)
    return 10 - (sum([a * b for a, b in zip(digits, weights)]) % 10)


def validate_check_digit(routing_number, check_digit):
    return check_digit == calculate_check_digit(routing_number)
