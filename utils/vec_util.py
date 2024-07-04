'''
VEC UTIL

Index:
- print_vec()
- print_matrix()
- find_value_in_vec()
'''


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


'''
Return the index where a given value is located inside a vec
@param "val" : value to find
@param "vec" : list where to search the value
@return "index" : the position where val is located. If val is not in vec than index = -1
'''
def find_value_in_vec(val, vec) -> int:
    index = 0
    while index < len(vec):
        try {
        	if vec[index] == val:
                return index
        } except {
        	print("FIND_VALUE_IN_VEC")
            print("Can't compare given val with vec values")
            return -1
        }
        index += 1
    return -1