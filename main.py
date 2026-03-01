import test_cases

def getMax(matrix):
    max = -1
    for i in matrix:
        for j in i:
            if j > max:
                max = j
    return max

def exists(n, matrix):
    for row in matrix:
        if n in row:
            return True
    return False

def set_values(matrix, value):
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            if matrix[row][column] != 0:
                matrix[row][column] = value

def rotate_90(matrix):
    #Transposition algorithm
    for i in range(len(matrix)):
        for j in range(len(matrix)-i):
            matrix[i+j][i], matrix[i][i+j] = matrix[i][i+j], matrix[i+j][i]

    mirror(matrix)

def mirror(matrix):
    for i in matrix:
        for j in range(len(matrix) // 2):
            i[j], i[-j-1] = i[-j-1], i[j]
    

#change alll functions to use a_b instead of camel case
def removeColumn(n, matrix):
    for row in matrix:
        row.pop(n)

#Get a more descriptive function name
#Check if the function works for larger matrices
def make_square(matrix, cols_to_rem):
    #Could potentially add check to see if input matrix is correct size but would slow process
    for _ in range(cols_to_rem):
        column_removed = False
        for i in range(len(matrix[0])):
            if matrix[-2][i] == 0:
                for j in matrix:
                    if j[i] != 0:
                        break
                else:
                    removeColumn(i, matrix)
                    column_removed = True
            if column_removed == True:
                break

def get_left_corner(matrix):
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            if matrix[row][column] != 0:
                corner = [row, 0]
                break
        else:
            continue
        break

    for column in range(len(matrix[0])):
        for row in range(len(matrix)):
            if matrix[row][column] != 0:
                corner[1] = column
                break
        else:
            continue
        break

    return corner

def get_right_corner(matrix):
    for row in range(len(matrix)-1, -1, -1):
        for column in range(len(matrix[0]) - 1, -1, -1):
            if matrix[row][column] != 0:
                corner = [row, 0]
                break
        else:
            continue
        break

    for column in range(len(matrix[0])-1, -1, -1):
        for row in range(len(matrix) - 1, -1, -1):
            if matrix[row][column] != 0:
                corner[1] = column
                break
        else:
            continue
        break

    return corner

#shift so corner is always left aligned
def format_polyomino(matrix, n):
    empty_rows = 0
    counter = 0
    while (n - empty_rows) > ((n+1) // 2):
        empty_rows = 0
        for i in matrix:
            if not(any(i)):
                empty_rows += 1
        
        if (n - empty_rows) > ((n+1) // 2):
            rotate_90(matrix)
            counter += 1

        if counter > 4:
            #Find correct error type
            for i in matrix:
                print(i)
            #returning an error for any n above 5
            raise ValueError(f"Infinite loop")
    
    while len(matrix) > (n+1) // 2:
        for row in range(len(matrix)):
            if not(any(matrix[row])):
                matrix.pop(row)
                break

    while len(matrix[0]) > n:
        for column in range(len(matrix[0])):
            for row in matrix:
                if row[column] != 0:
                    break
            else:
                removeColumn(column, matrix)
                continue
            break


    # get number of empty rows
    # check if number of empty rows is enough
    # if not rotate

    #n long, (n+1 // 2) high

def check_equality(input, target):
    input_corners = get_left_corner(input), get_right_corner(input)
    target_corners = get_left_corner(target), get_right_corner(target)

    #input_left_corner = [input_reference[0], input_reference[1] - target_reference[1]]

    #target_left_corner = [target_reference[0], 0]

    input_size = input_corners[1][0] - input_corners[0][0], input_corners[1][1] - input_corners[0][1]
    target_size = target_corners[1][0] - target_corners[0][0], target_corners[1][1] - target_corners[0][1]

    if input_size != target_size:
        return False
    
    equality = True

    #Checks translational equality
    for row in range(target_corners[0][0], target_corners[1][0]):
        for column in range(target_corners[0][1], target_corners[1][1]):
            if input[input_corners[0][0] + row - target_corners[0][0]][input_corners[0][1] + column - target_corners[0][1]] != target[row][column]:
                equality = False
                return equality

    return equality

def check_redundance(current_shape, shapes_arr, n):
    make_square(current_shape, cols_to_rem = n-1 - n // 2)
    for i in range(4):
        for j in shapes_arr:
            if check_equality(current_shape, j):
                redundant_shape = True
                break
        else:
            rotate_90(current_shape)
            continue
        break
    else:
        redundant_shape = False

    if redundant_shape == True:
        return redundant_shape

    mirror(current_shape)

    for i in range(4):
        for j in shapes_arr:
            if check_equality(current_shape, j):
                redundant_shape = True
                break
        else:
            rotate_90(current_shape)
            continue
        break
    else:
        redundant_shape = False
    
    return redundant_shape

def try_add_shape(new_shape, shapes, n):
    if check_redundance(new_shape, shapes, n) == False:
        print("----------")
        for i in new_shape:
            print(i)
        print("----------")
        format_polyomino(new_shape, n)
        shapes.append(new_shape)    

def extend_shape(previous_shape, rows, columns, n, shapes):
    matrix = [[0 for _ in range(columns+2)] for _ in range(rows+2)]
    
    for i in range(len(previous_shape)):
        for j in range(len(previous_shape[0])):
            matrix[i+1][j+1] = previous_shape[i][j]

    for row in range(len(matrix)-2):    
        for column in range(len(matrix[0])-2):
            if matrix[row+1][column+1] == 0:
                continue
            if matrix[row+1][column] == 0:
                new_shape = [row.copy() for row in matrix]
                new_shape[row+1][column] = n
                try_add_shape(new_shape, shapes, n)

            if matrix[row][column+1] == 0:
                new_shape = [row.copy() for row in matrix]
                new_shape[row][column+1] = n
                try_add_shape(new_shape, shapes, n)

            if matrix[row+1][column+2] == 0:
                new_shape = [row.copy() for row in matrix]
                new_shape[row+1][column+2] = n
                try_add_shape(new_shape, shapes, n)

            if matrix[row+2][column+1] == 0:
                new_shape = [row.copy() for row in matrix]
                new_shape[row+2][column+1] = n
                try_add_shape(new_shape, shapes, n)
    
    return shapes


a = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 4, 4, 4, 0],
    [0, 4, 0, 0, 0]
]

b = [
    [0, 0, 0, 4],
    [0, 4, 4, 4]
]

c = [
    [0, 0, 0, 4],
    [0, 4, 4, 4],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

d = [
    [0, 0, 0, 4],
    [0, 4, 4, 4],
]

i = [
    [0, 0, 0, 0],
    [0, 4, 4, 4],
    [0, 0, 0, 4],
    [0, 0, 0, 0]
]

t = [
    [4, 4, 4, 4],
    [0, 0, 0, 0]
]

test_arr = [[
    [0, 4, 0, 0],
    [0, 4, 4, 4]
]]

new = [
    [0, 0, 4, 0, 0],
    [0, 0, 4, 0, 0],
    [0, 0, 4, 4, 0],
    [0, 0, 0, 0, 0]
]

#mirror(a)

#for i in a:
#    print(i)
#print(check_equality(i, t))

#print(check_equality(a,b))

print(check_redundance(new, test_arr, 4))
#print(check_equality(c,d))

#format_polyomino(c, 4)

def returnShapes(n):
    if n == 1:
        return [[
                [n]
                ]]
    elif n == 2:
        return [[
                [n, n]
                ]]
    elif n < 0 or n > 17:
        raise ValueError(f"n must be between 0 and 17 not {n}")
    
    shapes = []
    generated_shapes = []

    rows = (n+1) // 2
    columns = n

    previous_shapes = returnShapes(n-1)

    for shape in previous_shapes:
        set_values(shape, n)

    for unique_shape in previous_shapes:
        shapes = generated_shapes[:]
        created_shapes = extend_shape(unique_shape, rows, columns, n, shapes)
        for new_shape in created_shapes:
            generated_shapes.append(new_shape)

    return generated_shapes

    # output -> [n, 0, 0]  [0, 0, 0]
    #           [n, n, 0]  [n, n, n]

    #take all the old shapes
    #for i in 
    #add squares to adjacent blocks 
    #check if it's a new shape 
    #add it to the list
    #shapes.append(new_shape)

    #returnShapes(n-1)

num = 4
a = returnShapes(num)

for i in a:
    for j in i:
        print(j)
    print("-------------")

#Expected number of polyominos for each k-1
polyominos_series = [1, 1, 2, 5, 12, 35, 108, 369, 1285, 4655, 17073, 63600, 238591, 901971, 3426576, 13079255]

if len(a) == polyominos_series[num-1]:
    print(f"CORRECT: {polyominos_series[num-1]}")
else:
    print(f"INCORRECT \n LENGTH: {len(a)} \n TARGET: {polyominos_series[num-1]}")

#for i in a :
#    for j in range(len(i)):
#        print(i)
#        i[j], i[-j] = i[-j], i[j]
#    print(i)

"""
Key rules:
You cannot overwrite other numbers
The number denotes the number of times is must be in the grid
The shape created by a number pattern must be fully orthogonal
Each section of numbers must reuse the shape of the previous section
Reflections and rotations of the shape are allowed
"""



#print(test_cases.test_shell)
#print(test_cases.subtiles1[0][0])


