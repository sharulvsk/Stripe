import sys

REGISTERED_NAMES = set()
SUFFIXES = {"inc", "corp", "llc", "l.l.c"}


def normalize(name: str) -> str:
    if name is None:
        return ""

    # 1. Case-insensitive
    result = name.lower()

    # 2. Replace separators with spaces
    result = result.replace("&", " ").replace(",", " ")

    # 3. Collapse spaces
    result = " ".join(result.split())
    if not result:
        return ""

    # 4. Remove leading articles
    if result.startswith("the "):
        result = result[4:]
    elif result.startswith("an "):
        result = result[3:]
    elif result.startswith("a "):
        result = result[2:]

    # 5. Remove "and" unless first word
    words = result.split()
    if len(words) > 1:
        words = [words[0]] + [w for w in words[1:] if w != "and"]
        result = " ".join(words)

    # 6. Remove company suffixes
    words = result.split()
    while words and words[-1] in SUFFIXES:
        words.pop()

    return " ".join(words).strip()


def main():
    lines = sys.stdin.read().strip().splitlines()
    i = 0

    # Load existing registered names
    n = int(lines[i]); i += 1
    for _ in range(n):
        normalized = normalize(lines[i]); i += 1
        if normalized:
            REGISTERED_NAMES.add(normalized)

    # Process availability requests
    m = int(lines[i]); i += 1
    for _ in range(m):
        account_id, proposed_name = lines[i].split("|", 1)
        i += 1

        normalized = normalize(proposed_name)

        if not normalized or normalized in REGISTERED_NAMES:
            print(f"{account_id}|Name Not Available")
        else:
            print(f"{account_id}|Name Available")
            REGISTERED_NAMES.add(normalized)  # permanently register


if __name__ == "__main__":
    main()
