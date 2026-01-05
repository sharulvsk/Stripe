import sys

REGISTERED_NAMES = {}   # normalized_name -> account_id
SUFFIXES = {"inc", "corp", "llc", "l.l.c"}


def normalize(name: str) -> str:
    if name is None:
        return ""

    # lower-case
    result = name.lower()

    # replace separators
    result = result.replace("&", " ").replace(",", " ")

    # collapse spaces
    result = " ".join(result.split())
    if not result:
        return ""

    # remove leading articles
    if result.startswith("the "):
        result = result[4:]
    elif result.startswith("an "):
        result = result[3:]
    elif result.startswith("a "):
        result = result[2:]

    # remove "and" unless first word
    words = result.split()
    if len(words) > 1:
        words = [words[0]] + [w for w in words[1:] if w != "and"]
        result = " ".join(words)

    # remove company suffixes
    words = result.split()
    while words and words[-1] in SUFFIXES:
        words.pop()

    return " ".join(words).strip()


def handle_registration(line: str):
    account_id, proposed_name = line.split("|", 1)
    normalized = normalize(proposed_name)

    if not normalized or normalized in REGISTERED_NAMES:
        print(f"{account_id}|Name Not Available")
    else:
        print(f"{account_id}|Name Available")
        REGISTERED_NAMES[normalized] = account_id


def handle_reclaim(line: str):
    # format: RECLAIM,account_id,original_proposed_name
    _, account_id, original_name = line.split(",", 2)
    normalized = normalize(original_name)

    # only original owner may reclaim
    if normalized in REGISTERED_NAMES and REGISTERED_NAMES[normalized] == account_id:
        del REGISTERED_NAMES[normalized]


def main():
    lines = sys.stdin.read().strip().splitlines()
    i = 0

    # bootstrap registered names
    n = int(lines[i]); i += 1
    for _ in range(n):
        normalized = normalize(lines[i]); i += 1
        if normalized:
            REGISTERED_NAMES[normalized] = "__SYSTEM__"

    # process requests
    m = int(lines[i]); i += 1
    for _ in range(m):
        line = lines[i]; i += 1
        if line.startswith("RECLAIM,"):
            handle_reclaim(line)
        else:
            handle_registration(line)


if __name__ == "__main__":
    main()
