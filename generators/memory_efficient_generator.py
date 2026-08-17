import json
import os

#memory fixes
jsonl_reader = True
jsonl_writer = True
hash_seen = True

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
    if hash_seen:
        #store hashes of standard forms instead of the tuples themselves
        if hash(standard_form(current_shape)) in seen:
            return True
        else:
            return False

    if standard_form(current_shape) in seen:
        return True
    else:
        return False

def try_add_shape(new_shape, shapes, n, seen):
    if check_redundance(new_shape, seen, n) == False:
        new_shape = format_polyomino(new_shape)
        if hash_seen:
            seen.add(hash(standard_form(new_shape)))
        else:
            seen.add(standard_form(new_shape))
        if jsonl_writer:
            #write the shape straight to the file instead of keeping it in memory
            shapes.write(json.dumps(sorted(new_shape)) + "\n")
        else:
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
        return [{
                (0, 0)
                }]
    elif n == 2:
        return [{
                (0, 0), (0, 1)
                }]
    elif n < 1 or n > 17:
        raise ValueError(f"n must be between 1 and 17 not {n}")

    if jsonl_writer and jsonl_reader == False:
        raise ValueError("jsonl_writer only works with jsonl_reader turned on")

    shapes = []
    generated_shapes = []
    seen = set()

    rows = (n+1) // 2
    columns = n

    if jsonl_reader:
        #make sure the previous generation is saved to a file first
        if os.path.exists(f"results/memory_efficient/polyominoes_{n-1}.jsonl") == False:
            if jsonl_writer and n-1 > 2:
                #the writer saves its own file as it generates
                returnShapes(n-1, use_saved)
            else:
                save_shapes(returnShapes(n-1, use_saved), n-1)

        if jsonl_writer:
            os.makedirs("results/memory_efficient", exist_ok=True)
            generated_shapes = open(f"results/memory_efficient/polyominoes_{n}.jsonl", "w")

        #read the previous shapes back one line at a time instead of all at once
        with open(f"results/memory_efficient/polyominoes_{n-1}.jsonl") as file:
            for line in file:
                previous_shape = set()
                for cell in json.loads(line):
                    previous_shape.add((cell[0], cell[1]))
                extend_shape(previous_shape, rows, columns, n, generated_shapes, seen)

        if jsonl_writer:
            generated_shapes.close()
            return len(seen)

        return generated_shapes

    if use_saved:
        try:
            with open(f"results/memory_efficient/polyominoes_{n-1}.json") as file:
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

def save_shapes(shapes, n):
    os.makedirs("results/memory_efficient", exist_ok=True)

    #save one shape per line so they can be read back one at a time
    if jsonl_reader:
        with open(f"results/memory_efficient/polyominoes_{n}.jsonl", "w") as file:
            for shape in shapes:
                file.write(json.dumps(sorted(shape)) + "\n")
        return

    shapes_as_lists = []
    for shape in shapes:
        shapes_as_lists.append(sorted(shape))
    with open(f"results/memory_efficient/polyominoes_{n}.json", "w") as file:
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

if __name__ == "__main__":
    num = 15
    a = returnShapes(num, use_saved=True)

    if jsonl_writer:
        #the shapes were already written to their file during generation
        length = a
    else:
        save_shapes(a, num)
        length = len(a)

    #for i in a:
    #    print_shape(i, num)
    #    print("-------------")

    #Expected number of polyominos for each k-1
    polyominos_series = [1, 1, 2, 5, 12, 35, 108, 369, 1285, 4655, 17073, 63600, 238591, 901971, 3426576, 13079255, 50107909]

    if length == polyominos_series[num-1]:
        print(f"CORRECT: \n LENGTH: {length} \n TARGET: {polyominos_series[num-1]}")
    else:
        print(f"INCORRECT \n LENGTH: {length} \n TARGET: {polyominos_series[num-1]}")

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

