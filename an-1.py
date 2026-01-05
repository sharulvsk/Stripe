import sys

SUFFIXES = {"inc", "corp", "llc", "l.l.c"}
registered_names = set()


def normalize(name: str) -> str:
    if not name:
        return ""

    # 1. Ignore case
    result = name.lower()

    # 2. Treat separators as spaces
    result = result.replace("&", " ").replace(",", " ")

    # (optional improvement) remove punctuation like "."
    result = result.replace(".", " ")

    # 3. Collapse spaces
    result = " ".join(result.split())
    if not result:
        return ""

    # 4. Remove leading articles
    for article in ("the ", "an ", "a "):
        if result.startswith(article):
            result = result[len(article):].strip()
            break

    # 5. Remove "and" unless it's the first word
    words = result.split()
    if len(words) > 1:
        words = [words[0]] + [w for w in words[1:] if w != "and"]
        result = " ".join(words)

    # 6. Remove suffixes
    words = result.split()
    while words and words[-1] in SUFFIXES:
        words.pop()

    result = " ".join(words).strip()
    return result


def main():
    lines = sys.stdin.read().strip().splitlines()
    idx = 0

    # Read existing registered names
    n = int(lines[idx]); idx += 1
    for _ in range(n):
        normalized = normalize(lines[idx]); idx += 1
        if normalized:
            registered_names.add(normalized)

    # Process availability requests
    m = int(lines[idx]); idx += 1
    for _ in range(m):
        line = lines[idx]; idx += 1

        parts = line.split("|", 2)
        if len(parts) < 2:
            continue  # ignore bad input

        account_id, proposed_name = parts[0], parts[1]
        normalized = normalize(proposed_name)

        if not normalized or normalized in registered_names:
            print(f"{account_id}|Name Not Available")
        else:
            print(f"{account_id}|Name Available")
            registered_names.add(normalized)


if __name__ == "__main__":
    main()
