import csv
import sys

MATCH_SCORE = 1
MISMATCH_SCORE = -1
GAP_PENALTY = -2


def needleman_wunsch(sequence1, sequence2):
    """
    Perform Needleman-Wunsch algorithm on two sequences.

    parameters
    - sequence1 (str): The first sequence.
    - sequence2 (str): The second sequence.

    Returns
    - aligned_seq1 (str): The aligned first sequence.
    - aligned_seq2 (str): The aligned second sequence.
    - alignment_score (int): The alignment score.
    """
    score_matrix = [[0] * (len(sequence2) + 1)
                    for _ in range(len(sequence1) + 1)]

    traceback_matrix = [[''] * (len(sequence2) + 1)
                        for _ in range(len(sequence1) + 1)]

    # First Line and Column of matrices
    for i in range(1, len(sequence1) + 1):
        score_matrix[i][0] = GAP_PENALTY * i
        traceback_matrix[i][0] = 'U'  # Up

    for j in range(1, len(sequence2) + 1):
        score_matrix[0][j] = GAP_PENALTY * j
        traceback_matrix[0][j] = 'L'  # Left

    # Fill in the matrices
    for i in range(1, len(sequence1) + 1):
        for j in range(1, len(sequence2) + 1):
            match_score = score_matrix[i-1][j-1] + \
                (MATCH_SCORE if sequence1[i-1] ==
                 sequence2[j-1] else MISMATCH_SCORE)
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
    _route = ''
    i, j = len(sequence1), len(sequence2)

    while i > 0 or j > 0:
        direction = traceback_matrix[i][j]
        move = direction[-1] if direction else ''
        if move == 'D':
            aligned_seq1 = sequence1[i-1] + aligned_seq1
            aligned_seq2 = sequence2[j-1] + aligned_seq2
            i -= 1
            j -= 1
            _route += 'D'
        elif move == 'U':
            aligned_seq1 = sequence1[i-1] + aligned_seq1
            aligned_seq2 = '-' + aligned_seq2
            i -= 1
            _route += 'U'
        elif move == 'L':
            aligned_seq1 = '-' + aligned_seq1
            aligned_seq2 = sequence2[j-1] + aligned_seq2
            j -= 1
            _route += 'L'

    # Reverse the route to match reading direction
    _route = _route[::-1]

    # Calculate score
    alignment_score = 0

    for a, b in zip(aligned_seq1, aligned_seq2):
        if a == b:
            alignment_score += MATCH_SCORE
        elif a == '-' or b == '-':
            alignment_score += GAP_PENALTY
        else:
            alignment_score += MISMATCH_SCORE

    return aligned_seq1, aligned_seq2, alignment_score, _route


def main():
    """
    Read the input file and perform Needleman-Wunsch algorithm on each pair of sequences.

    The input file should be a CSV file with two columns, each containing a sequence.

    The output will be the aligned sequences and the alignment score.
    """
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                seq1, seq2 = row
                aligned_seq1, aligned_seq2, alignment_score, _route = needleman_wunsch(
                    seq1, seq2)
                print(f"{aligned_seq1} {aligned_seq2} {alignment_score}")


if __name__ == "__main__":
    main()
