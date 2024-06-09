'''
Print a python list in terminal
@param "vec" : a python list
'''
def print_vec(vec):
    for item in vec:
        print(item)


'''
Print a python matrix in terminal
@param "matrix" : a python matrix
'''
def print_matrix(matrix):
    for row in matrix:
        for item in row:
            print(item, end=", ")