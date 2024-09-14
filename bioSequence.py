import csv
import sys

MATCH_SCORE = 1
MISMATCH_SCORE = -1
GAP_PENALTY = -2


def needleman_wunsch(seq1, seq2):

    score_matrix = [[0] * (len(seq2) + 1) for _ in range(len(seq1) + 1)]

    traceback_matrix = [[''] * (len(seq2) + 1) for _ in range(len(seq1) + 1)]

    # First Line and Column of matrices
    for i in range(1, len(seq1) + 1):
        score_matrix[i][0] = GAP_PENALTY * i
        traceback_matrix[i][0] = 'U'  # Up

    for j in range(1, len(seq2) + 1):
        score_matrix[0][j] = GAP_PENALTY * j
        traceback_matrix[0][j] = 'L'  # Left

    # Fill in the matrices
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            match_score = score_matrix[i-1][j-1] + \
                (MATCH_SCORE if seq1[i-1] == seq2[j-1] else MISMATCH_SCORE)
            delete_score = score_matrix[i-1][j] + GAP_PENALTY
            insert_score = score_matrix[i][j-1] + GAP_PENALTY
            max_score = max(match_score, delete_score, insert_score)

            score_matrix[i][j] = max_score

            if max_score == match_score:
                traceback_matrix[i][j] += 'D'  # Diagonal
            if max_score == delete_score:
                traceback_matrix[i][j] += 'U'  # Up
            if max_score == insert_score:
                traceback_matrix[i][j] += 'L'  # Left

    # Perform traceback and record the route
    aligned_seq1 = ''
    aligned_seq2 = ''
    route = ''
    i, j = len(seq1), len(seq2)

    while i > 0 or j > 0:
        direction = traceback_matrix[i][j]
        move = direction[-1] if direction else ''
        if move == 'D':
            aligned_seq1 = seq1[i-1] + aligned_seq1
            aligned_seq2 = seq2[j-1] + aligned_seq2
            i -= 1
            j -= 1
            route += 'D'
        elif move == 'U':
            aligned_seq1 = seq1[i-1] + aligned_seq1
            aligned_seq2 = '-' + aligned_seq2
            i -= 1
            route += 'U'
        elif move == 'L':
            aligned_seq1 = '-' + aligned_seq1
            aligned_seq2 = seq2[j-1] + aligned_seq2
            j -= 1
            route += 'L'

    # Reverse the route to match reading direction
    route = route[::-1]

    # Calculate score
    alignment_score = 0

    for a, b in zip(aligned_seq1, aligned_seq2):
        if a == b:
            alignment_score += MATCH_SCORE
        elif a == '-' or b == '-':
            alignment_score += GAP_PENALTY
        else:
            alignment_score += MISMATCH_SCORE

    return aligned_seq1, aligned_seq2, alignment_score, route


def main():
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                seq1, seq2 = row
                aligned_seq1, aligned_seq2, alignment_score, route = needleman_wunsch(
                    seq1, seq2)
                print(f"{aligned_seq1} {aligned_seq2} {alignment_score}")


if __name__ == "__main__":
    main()
