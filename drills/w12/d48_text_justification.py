"""d48 Text justification: full-justify words into lines of width w. Extra spaces distributed left-heavy; a line with one
word and the last line are left-justified and padded on the right."""


def justify(words: list, w: int) -> list:
    lines, i = [], 0
    while i < len(words):
        j, length = i, 0
        while j < len(words) and length + len(words[j]) + (j - i) <= w:
            length += len(words[j])
            j += 1
        line_words = words[i:j]
        gaps = len(line_words) - 1
        if j == len(words) or gaps == 0:
            line = " ".join(line_words)
            lines.append(line + " " * (w - len(line)))
        else:
            spaces = w - length
            q, r = divmod(spaces, gaps)
            line = ""
            for k, word in enumerate(line_words[:-1]):
                line += word + " " * (q + (1 if k < r else 0))
            lines.append(line + line_words[-1])
        i = j
    return lines
