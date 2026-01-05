def expand_string(inp: str):
    output = []
    open_idx = inp.find('{')
    close_idx = inp.find('}')
    if open_idx == -1 or close_idx == -1 or close_idx < open_idx:
        output.append(inp)
        return output
    pre = inp[:open_idx]
    suf = inp[close_idx + 1:]
    middle = inp[open_idx + 1:close_idx]

    parts = middle.split(",")
    if len(parts) < 2:
        output.append(inp)
        return output

    for p in parts:
        output.append(pre + p + suf)

    return output
def main():
    inp = input().strip()
    result = expand_string(inp)

    for s in result:
        print(s)


if __name__ == "__main__":
    main()
