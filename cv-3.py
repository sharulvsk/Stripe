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

    # VISA
    if length == 16 and card_number.startswith("4"):
        return "VISA"

    # MASTERCARD
    if length == 16:
        prefix = int(card_number[:2])
        if 51 <= prefix <= 55:
            return "MASTERCARD"

    # AMEX
    if length == 15 and (card_number.startswith("34") or card_number.startswith("37")):
        return "AMEX"

    return "UNKNOWN_NETWORK"


def validate(card_number: str) -> str:
    # 1. Corrupted check — invalid chars other than digits, * or X
    for ch in card_number:
        if not (ch.isdigit() or ch == "*" or ch == "X"):
            return "CORRUPTED"

    # 2. Redacted
    if "*" in card_number or "X" in card_number:
        return "REDACTED"

    # 3. Network detection
    network = detect_network(card_number)
    if network == "UNKNOWN_NETWORK":
        return "UNKNOWN_NETWORK"

    # 4. Luhn checksum
    if not is_valid_luhn(card_number):
        return "INVALID_CHECKSUM"

    return network


# Example tests
if __name__ == "__main__":
    print(validate("4242424242424242"))      # VISA
    print(validate("4242********4242"))      # REDACTED
    print(validate("4242********4242"))      # REDACTED
    print(validate("4242-4242-4242-4242"))   # CORRUPTED
    print(validate("378282246310005"))       # AMEX
    print(validate("5112345678901234"))      # INVALID_CHECKSUM
    print(validate("562523348109901"))       # UNKNOWN_NETWORK
