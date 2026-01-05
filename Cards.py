import sys

class Interval:
    def __init__(self, start, end, brand):
        self.start = start
        self.end = end
        self.brand = brand

def main():
    data = sys.stdin.read().strip().splitlines()
    bin_prefix = data[0].strip()          # 6-digit BIN
    n = int(data[1].strip())

    intervals = []
    for i in range(2, 2 + n):
        parts = data[i].split(",")
        start = int(parts[0])
        end = int(parts[1])
        brand = parts[2]
        intervals.append(Interval(start, end, brand))

    # Sort by start offset
    intervals.sort(key=lambda iv: iv.start)

    result = []
    current = 0
    MAX = 9_999_999_999

    for iv in intervals:
        # Gap before this interval
        if iv.start > current:
            fill_brand = iv.brand if not result else result[-1].brand
            result.append(Interval(current, iv.start - 1, fill_brand))

        # Add current interval
        result.append(Interval(iv.start, iv.end, iv.brand))
        current = iv.end + 1

    # Gap after last interval
    if current <= MAX and result:
        last_brand = result[-1].brand
        result.append(Interval(current, MAX, last_brand))

    # Output full 16-digit card numbers
    for iv in result:
        start_card = bin_prefix + f"{iv.start:010d}"
        end_card = bin_prefix + f"{iv.end:010d}"
        print(f"{start_card},{end_card},{iv.brand}")

if __name__ == "__main__":
    main()
