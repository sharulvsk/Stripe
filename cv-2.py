def is_valid_luhn(number: str) -> bool:
    total = 0
    double_digit = False

    for ch in reversed(number):
        digit = ord(ch) - ord('0')

        if double_digit:
            digit *= 2
            if digit > 9:
                digit -= 9

        total += digit
        double_digit = not double_digit

    return total % 10 == 0


def detect_network(card_number: str) -> str:
    length = len(card_number)

    # VISA (16 digits, starts with 4)
    if length == 16 and card_number.startswith("4"):
        return "VISA"

    # MASTERCARD (16 digits, prefix 51–55)
    if length == 16:
        prefix = int(card_number[:2])
        if 51 <= prefix <= 55:
            return "MASTERCARD"

    # AMEX (15 digits, starts with 34 or 37)
    if length == 15 and (card_number.startswith("34") or card_number.startswith("37")):
        return "AMEX"

    return "UNKNOWN_NETWORK"


def validate(card_number: str) -> str:
    network = detect_network(card_number)

    if network == "UNKNOWN_NETWORK":
        return "UNKNOWN_NETWORK"

    if not is_valid_luhn(card_number):
        return "INVALID_CHECKSUM"

    return network


# Example tests
if __name__ == "__main__":
    print(validate("54823345909943"))      # UNKNOWN_NETWORK
    print(validate("442523348109994"))     # VISA
    print(validate("562523348109901"))     # UNKNOWN_NETWORK
