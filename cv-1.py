def is_valid_luhn(number: str) -> bool:
    total = 0
    double_digit = False

    # iterate from right to left
    for ch in reversed(number):
        digit = ord(ch) - ord('0')

        if double_digit:
            digit *= 2
            if digit > 9:
                digit -= 9

        total += digit
        double_digit = not double_digit

    return total % 10 == 0


def validate_visa(card_number: str) -> str:
    # Part-1 assumptions:
    # - input is 16 digits
    # - starts with '4'
    if not is_valid_luhn(card_number):
        return "INVALID_CHECKSUM"
    return "VISA"


# Example test cases
if __name__ == "__main__":
    print(validate_visa("4532015112830366"))  # VISA
    print(validate_visa("4242424242424243"))  # INVALID_CHECKSUM
