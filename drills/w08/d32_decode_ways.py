"""d32 Decode ways: digits map A=1 ... Z=26. Number of ways to decode s. "06" is invalid (0 ways)."""


def num_decodings(s: str) -> int:
    if not s:
        return 0
    prev2, prev1 = 1, (1 if s[0] != "0" else 0)  # dp[i-2], dp[i-1]
    for i in range(1, len(s)):
        cur = prev1 if s[i] != "0" else 0
        if 10 <= int(s[i - 1:i + 1]) <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1
