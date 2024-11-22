import sys
import ast

# Define an infinity value for no connection
INF = float('inf')

def floyd_warshall(matrix):
    # Get the number of vertices (assumed to be square matrix)
    n = len(matrix)
    
    # Initialize the distance matrix with the given adjacency matrix
    dist = [[matrix[i][j] for j in range(n)] for i in range(n)]

    # List of intermediate matrices
    matrices = [dist]

    # Floyd-Warshall algorithm
    for k in range(n):
        next_matrix = [[dist[i][j] for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                if next_matrix[i][k] != INF and next_matrix[k][j] != INF:
                    next_matrix[i][j] = min(next_matrix[i][j], next_matrix[i][k] + next_matrix[k][j])
        matrices.append(next_matrix)
        dist = next_matrix

    return matrices

def process_input(cost_adj_matrix_str, k):
    # Preprocess the input string to replace 'inf' with a placeholder
    cost_adj_matrix_str = cost_adj_matrix_str.replace('inf', '"INF_PLACEHOLDER"')

    # Convert the string input to a list using ast.literal_eval
    cost_adj_matrix = ast.literal_eval(cost_adj_matrix_str)

    # Replace the 'INF_PLACEHOLDER' with float('inf')
    for i in range(len(cost_adj_matrix)):
        for j in range(len(cost_adj_matrix[i])):
            if cost_adj_matrix[i][j] == "INF_PLACEHOLDER":
                cost_adj_matrix[i][j] = INF

    # Run Floyd-Warshall algorithm
    floyd_warshall_matrices = floyd_warshall(cost_adj_matrix)

    # Return the k-th matrix or 0-th if k=0 (the original adjacency matrix)
    return floyd_warshall_matrices[k]

if __name__ == "__main__":
    # Only proceed if command line arguments are provided
    if len(sys.argv) > 1:
        # Read inputs from the command line
        cost_adj_matrix_str = sys.argv[1]
        k = int(sys.argv[2])

        # Get the result matrix for the given k
        result_matrix = process_input(cost_adj_matrix_str, k)

        # Replace INF back with 'inf' for the final output
        for i in range(len(result_matrix)):
            for j in range(len(result_matrix[i])):
                if result_matrix[i][j] == INF:
                    result_matrix[i][j] = float('inf')

        # Output result in the same format
        print(result_matrix)
