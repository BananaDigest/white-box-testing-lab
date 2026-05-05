def process_matrix(matrix):
    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                for k in range(matrix[i][j]):
                    count += k % 3
    return count
