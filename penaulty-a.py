def compute_penalty(log: str, closing_time: int) -> int:
    s = log.replace(" ", "")
    penalty = 0
    for i in range(min(closing_time, len(s))):
        if s[i] == 'N':      
            penalty += 1

    for i in range(closing_time, len(s)):
        if s[i] == 'Y':      
            penalty += 1
    return penalty
