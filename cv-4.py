def validate(card_number: str) -> str:
    # 1. CORRUPTED
    for c in card_number:
        if not (c.isdigit() or c == "*" or c == "X"):
            return "CORRUPTED"

    is_redacted = "*" in card_number or "X" in card_number

    # 2. Try network inference (even if redacted)
    inferred = infer_network(card_number)
    if is_redacted:
        return inferred if inferred != "UNKNOWN_NETWORK" else "REDACTED"

    # 3. Fully visible card
    network = detect_network(card_number)
    if network == "UNKNOWN_NETWORK":
        return "UNKNOWN_NETWORK"

    if not is_valid_luhn(card_number):
        return "INVALID_CHECKSUM"

    return network


# ================= NETWORK DETECTION =================

def detect_network(card_number: str) -> str:
    length = len(card_number)

    # VISA
    if length == 16 and card_number.startswith("4"):
        return "VISA"

    # MASTERCARD
    if length == 16 and len(card_number) >= 2:
        prefix = int(card_number[:2])
        if 51 <= prefix <= 55:
            return "MASTERCARD"

    # AMEX
    if length == 15 and (card_number.startswith("34") or card_number.startswith("37")):
        return "AMEX"

    return "UNKNOWN_NETWORK"


# ================= REDACTED INFERENCE =================

def infer_network(card_number: str) -> str:
    length = len(card_number)

    # VISA
    if length == 16 and card_number.startswith("4"):
        return "VISA"

    # MASTERCARD
    if length == 16 and len(card_number) >= 2 \
       and card_number[0].isdigit() and card_number[1].isdigit():
        prefix = int(card_number[:2])
        if 51 <= prefix <= 55:
            return "MASTERCARD"

    # AMEX
    if length == 15 and (card_number.startswith("34") or card_number.startswith("37")):
        return "AMEX"

    return "UNKNOWN_NETWORK"


# ================= LUHN =================

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


# ================= TEST =================

if __name__ == "__main__":
    print(validate("4242********4242"))   # VISA
    print(validate("37XXXXXXXXXXX005"))   # AMEX
    print(validate("5XXXXXXXXXXXXXXX"))   # REDACTED
    print(validate("4242-4242-4242-4242"))# CORRUPTED
    print(validate("4532015112830366"))   # VISA
    print(validate("5112345678901234"))   # INVALID_CHECKSUM
