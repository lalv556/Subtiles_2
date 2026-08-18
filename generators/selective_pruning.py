import json
import os

#the board whose clues are used for pruning
board_file = "boards/subtiles_2.txt"

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

def rotate_90(shape):
    #(row, column) -> (column, -row)
    rotated_shape = set()
    for cell in shape:
        rotated_shape.add((cell[1], -cell[0]))

    return format_polyomino(rotated_shape)

def mirror(shape):
    #(row, column) -> (row, -column)
    mirrored_shape = set()
    for cell in shape:
        mirrored_shape.add((cell[0], -cell[1]))

    return format_polyomino(mirrored_shape)

#change alll functions to use a_b instead of camel case

#shift so corner is always left aligned
def format_polyomino(shape):
    rows = []
    columns = []
    for cell in shape:
        rows.append(cell[0])
        columns.append(cell[1])

    min_row = min(rows)
    min_column = min(columns)

    formatted_shape = set()
    for cell in shape:
        formatted_shape.add((cell[0] - min_row, cell[1] - min_column))

    return formatted_shape

def standard_form(shape):
    #whichever orientation the shape is in, this always returns the same one
    orientations = []
    current_shape = format_polyomino(shape)
    for i in range(4):
        orientations.append(tuple(sorted(current_shape)))
        orientations.append(tuple(sorted(mirror(current_shape))))
        current_shape = rotate_90(current_shape)

    orientations.sort()
    return orientations[0]

def check_redundance(current_shape, seen, n):
    if standard_form(current_shape) in seen:
        return True
    else:
        return False

def try_add_shape(new_shape, shapes, n, seen):
    if check_redundance(new_shape, seen, n) == False:
        new_shape = format_polyomino(new_shape)
        seen.add(standard_form(new_shape))
        shapes.append(new_shape)

def extend_shape(previous_shape, rows, columns, n, shapes, seen):
    for cell in previous_shape:
        row = cell[0]
        column = cell[1]

        if ((row, column-1) in previous_shape) == False:
            new_shape = previous_shape.copy()
            new_shape.add((row, column-1))
            try_add_shape(new_shape, shapes, n, seen)

        if ((row-1, column) in previous_shape) == False:
            new_shape = previous_shape.copy()
            new_shape.add((row-1, column))
            try_add_shape(new_shape, shapes, n, seen)

        if ((row, column+1) in previous_shape) == False:
            new_shape = previous_shape.copy()
            new_shape.add((row, column+1))
            try_add_shape(new_shape, shapes, n, seen)

        if ((row+1, column) in previous_shape) == False:
            new_shape = previous_shape.copy()
            new_shape.add((row+1, column))
            try_add_shape(new_shape, shapes, n, seen)

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

#print(check_redundance(new, test_arr, 4))
#print(check_equality(c,d))

#format_polyomino(c, 4)

def returnShapes(n, use_saved=False):
    if n == 1:
        shapes = filter_shapes([{
                (0, 0)
                }], 1)
        save_shapes(shapes, 1)
        return shapes
    elif n == 2:
        shapes = filter_shapes([{
                (0, 0), (0, 1)
                }], 2)
        save_shapes(shapes, 2)
        return shapes
    elif n < 1 or n > 17:
        raise ValueError(f"n must be between 1 and 17 not {n}")

    shapes = []
    generated_shapes = []
    seen = set()

    rows = (n+1) // 2
    columns = n

    if use_saved:
        try:
            #the saved files already hold pruned shapes with valid ancestry
            with open(f"results/early_pruning/{board_name}/polyominoes_{n-1}.json") as file:
                previous_shapes = []
                for shape in json.load(file):
                    loaded_shape = set()
                    for cell in shape:
                        loaded_shape.add((cell[0], cell[1]))
                    previous_shapes.append(loaded_shape)
        except FileNotFoundError:
            previous_shapes = returnShapes(n-1, use_saved)
    else:
        previous_shapes = returnShapes(n-1)

    for unique_shape in previous_shapes:
        extend_shape(unique_shape, rows, columns, n, generated_shapes, seen)

    #filter before returning so pruned shapes never get extended
    shapes = filter_shapes(generated_shapes, n)
    save_shapes(shapes, n)
    return shapes

    # output -> [n, 0, 0]  [0, 0, 0]
    #           [n, n, 0]  [n, n, n]

    #take all the old shapes
    #for i in
    #add squares to adjacent blocks
    #check if it's a new shape
    #add it to the list
    #shapes.append(new_shape)

    #returnShapes(n-1)

def save_shapes(shapes, n):
    os.makedirs(f"results/early_pruning/{board_name}", exist_ok=True)
    shapes_as_lists = []
    for shape in shapes:
        shapes_as_lists.append(sorted(shape))
    with open(f"results/early_pruning/{board_name}/polyominoes_{n}.json", "w") as file:
        json.dump(shapes_as_lists, file)

def print_shape(shape, n):
    #draw the shape as a grid
    rows = []
    columns = []
    for cell in shape:
        rows.append(cell[0])
        columns.append(cell[1])

    for row in range(max(rows) + 1):
        line = []
        for column in range(max(columns) + 1):
            if (row, column) in shape:
                line.append(n)
            else:
                line.append(0)
        print(line)

def load_board(file_name):
    #the raw clue board, numbers and 0s, one grid
    board = []
    with open(file_name) as file:
        for line in file:
            row = line.split()
            if len(row) > 0:
                board.append(row)
    return board

def make_pattern(board, n):
    #build this n's pattern: keep n's clues, other clues become X, ring of X for the board edges
    width = len(board[0]) + 2
    pattern = [["X"] * width]
    for row in board:
        pattern_row = ["X"]
        for cell in row:
            if cell == str(n):
                pattern_row.append(cell)
            elif cell != "0":
                pattern_row.append("X")
            else:
                pattern_row.append("0")
        pattern_row.append("X")
        pattern.append(pattern_row)
    pattern.append(["X"] * width)
    return pattern

def check_placement(shape, pattern, row_shift, column_shift):
    for row in range(len(pattern)):
        for column in range(len(pattern[row])):
            covered = (row - row_shift, column - column_shift) in shape
            if pattern[row][column] == "X" and covered == True:
                return False
            if pattern[row][column] != "X" and pattern[row][column] != "0" and covered == False:
                return False
    return True

def matches_pattern(shape, pattern):
    #a shape is valid if any orientation fits anywhere on the pattern
    orientations = []
    current_shape = format_polyomino(shape)
    for i in range(4):
        orientations.append(current_shape)
        orientations.append(mirror(current_shape))
        current_shape = rotate_90(current_shape)

    for orientation in orientations:
        shape_rows = []
        shape_columns = []
        for cell in orientation:
            shape_rows.append(cell[0])
            shape_columns.append(cell[1])

        #the shape is allowed to hang over the edges of the pattern
        for row_shift in range(-max(shape_rows), len(pattern)):
            for column_shift in range(-max(shape_columns), len(pattern[0])):
                if check_placement(orientation, pattern, row_shift, column_shift) == True:
                    return True
    return False

def filter_shapes(shapes, n):
    #build this n's pattern from the board and keep only the shapes that match it
    pattern = make_pattern(board, n)
    filtered_shapes = []
    for shape in shapes:
        if matches_pattern(shape, pattern) == True:
            filtered_shapes.append(shape)
    return filtered_shapes

board = load_board(board_file)
#name the cache folder after the board so results from different boards dont mix
board_name = board_file.split("/")[-1].split(".")[0]

if __name__ == "__main__":
    num = 16
    a = returnShapes(num, use_saved=True)

    print(f"{len(a)} shapes match the patterns")
    for shape in a:
        print_shape(shape, num)
        print("-------------")

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
