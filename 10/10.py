import sys

close_open_map = {
    ")": "(",
    "}": "{",
    "]": "[",
    ">": "<",
}

syntax_error_score_table = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137, 
}

autocomplete_score_table = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

def find_first_error(line):
    """
    Find the first character causing a syntax error.
    
    If no first error, returns the stack of incomplete brackets.
    """
    ch_stack = []
    for ch in line:
        if ch in close_open_map.values():
            ch_stack.append(ch)
        elif ch in close_open_map.keys():
            if close_open_map[ch] == ch_stack[-1]:
                ch_stack.pop()
            else:
                return ch, ch_stack
    return None, ch_stack

def compute_scores(lines):
    """Get the syntax error score and autocomplete scores for the given lines."""
    syntax_error_score = 0
    autocomplete_scores = []
    for line in lines:
        error_bracket, incomplete_stack = find_first_error(line)
        if error_bracket:
            syntax_error_score += syntax_error_score_table[error_bracket]
        else:
            autocomplete_score = 0
            for ch in reversed(incomplete_stack):
                autocomplete_score *= 5
                autocomplete_score += autocomplete_score_table[ch]
            autocomplete_scores.append(autocomplete_score)
    return syntax_error_score, autocomplete_scores

def main():
    """Advent of Code Day 10."""
    lines = sys.stdin.readlines()
    syntax_error_score, autocomplete_scores = compute_scores(lines)
    print(syntax_error_score)
    autocomplete_scores.sort()
    print(autocomplete_scores[int(len(autocomplete_scores)/2)])

main()