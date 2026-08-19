"""
--- Solver guide ---
Load pruned sets

n_values =    [1, 2, 3, 4, 5 , 6 ,  7 ,  8 ,  9 ,  10 ,  11 , 12, 13,  14, 15, 16]
layer_sizes = [1, 1, 2, 5, 12, 31, 101, 344, 451, 2434, 6296, 2 , 28, 358, 54, 14]

Run a sweep to make sure at least one n+1 order shape contains an n order shape
Run a second sweep to make sure at least one n order shape is present in an n+1 order shape
Repeat this process until no shapes are removed

n_values =    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
layer_sizes = [1, 1, 2, 3, 4, 6, 5, 4, 3, 3 , 2 , 2 , 11, 19, 14, 14]

When sweep finishes stack pruned sets in a tree, cascaded by set size + print to console
Compute total list of possible branch paths to give a percentage log of how far through the tree the solver is
(if a node is skipped all the possible paths that node could have led to contribute to searched paths)

Reordered:
n_values =    [1, 2, 3, 11, 12, 4, 9, 10, 5, 8, 7, 6, 13, 15, 16, 14]
layer_sizes = [1, 1, 2, 2 , 2 , 3, 3, 3 , 4, 4, 5, 6, 11, 14, 14, 19]

total_branches = 4247147520

Do an in order traversal (depth first search) through the tree nodes, iteratively checking if a rotation, mirror or translation 
of a shape agrees with the grid.

If none of these options are compatible with the grid move onto the next node on the right
Check that larger n is derived from smaller n, if it isn't count node as incompatible
Do the same to check that smaller n order shapes can lead into larger n order shapes
If you go through a whole layer of a tree checking for every node and none is compatible break to previous node
Node then continues finding valid transpositions for shape
If every transposition for a shape has been exhausted, move onto the next node

If one of these options is compatible move down the tree and continue process

For a placement to be compatible with the grid it must satisfy 3 conditions:
1. Covers all number Ns present on the grid
2. Doesn't overlap with original numbers or the border
3. Doesn't overlap with a previously placed shape

Once a grid is computed that complies with these three conditions it is printed to the console
"""

import json

target = "subtiles_2"
board_file = "boards/subtiles_2.txt"

def check_upwards(small_list, large_list):
    possible_children = set()
    for shape in large_list:
        for cell in shape:
            smaller_shape = set(shape)
            smaller_shape.remove(cell)
            possible_children.add(standard_form(smaller_shape))

    kept = []
    for shape in small_list:
        if standard_form(shape) in possible_children:
            kept.append(shape)
    return kept

def check_downwards(small_list, large_list):
    valid_children = set()
    for shape in small_list:
        valid_children.add(standard_form(shape))

    kept = []
    for shape in large_list:
        for cell in shape:
            smaller_shape = set(shape)
            smaller_shape.remove(cell)
            if standard_form(smaller_shape) in valid_children:
                kept.append(shape)
                break
    return kept

def rotate_90(shape):
    rotated_shape = set()
    for cell in shape:
        rotated_shape.add((cell[1], -cell[0]))

    return format_polyomino(rotated_shape)

def mirror(shape):
    mirrored_shape = set()
    for cell in shape:
        mirrored_shape.add((cell[0], -cell[1]))

    return format_polyomino(mirrored_shape)

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
    orientations = []
    current_shape = format_polyomino(shape)
    for i in range(4):
        orientations.append(tuple(sorted(current_shape)))
        orientations.append(tuple(sorted(mirror(current_shape))))
        current_shape = rotate_90(current_shape)

    orientations.sort()
    return orientations[0]

def load_board(file_name):
    board = []
    with open(file_name) as file:
        for line in file:
            row = line.split()
            if len(row) > 0:
                board.append(row)
    return board

def board_constraints(board, n):
    constrained_board = []
    for row in board:
        constrained_board.append(row[:])

    for row in range(len(board)):
        for column in range(len(board[0])):
            if int(board[row][column]) == 0 or int(board[row][column]) == n:
                continue
            else:
                constrained_board[row][column] = "X"
    return constrained_board

def log_progress(current_depth):
    global run_percentage, last_logged_transpositions
    position = 0
    for depth in range(len(search_order)):
        position = position + node_index[depth] * paths_below[depth]

    percent = position / total_branches * 100
    percent = round(percent, 2)

    #only print if progress has moved forward or 1000 transpositions have passed
    if percent <= run_percentage and transpositions - last_logged_transpositions < 1000:
        return

    if percent > run_percentage:
        run_percentage = percent
    last_logged_transpositions = transpositions
    print(f"Branch progress: {run_percentage}%, transpositions tried: {transpositions}, chain depth: {current_depth + 1}/{len(search_order)} (n={search_order[current_depth]})")

def shape_key(shape):
    sorted_cells = sorted(shape)
    return tuple(sorted_cells)

def check_derivation(small_shape, large_shape):
    #the large shape must be the small shape plus one cell
    small = standard_form(small_shape)
    for cell in large_shape:
        smaller_shape = set(large_shape)
        smaller_shape.remove(cell)
        if standard_form(smaller_shape) == small:
            return True
    return False

def derived_from(small_shape, large_shape, seen_derivations):
    key = (shape_key(small_shape), shape_key(large_shape))
    if key in seen_derivations:
        return seen_derivations[key]

    answer = check_derivation(small_shape, large_shape)
    seen_derivations[key] = answer
    return answer

#save orientations
def get_orientations(n, node, shape, seen_orientations):
    if (n, node) not in seen_orientations:
        orientations = []
        current_shape = format_polyomino(shape)
        for i in range(4):
            orientations.append(current_shape)
            orientations.append(mirror(current_shape))
            current_shape = rotate_90(current_shape)
        seen_orientations[(n, node)] = orientations

    return seen_orientations[(n, node)]

def solve(depth, occupied, chosen):
    global solution, transpositions
    if solution != None:
        return
    if depth == len(search_order):
        solution = chosen
        total_layers = len(search_order)
        print(f"Branch progress: {run_percentage}%, transpositions tried: {transpositions}, chain depth: {total_layers}/{total_layers}")
        return

    current_n = search_order[depth]

    clue_rows = []
    clue_columns = []
    for cell in clue_cells[current_n]:
        clue_rows.append(cell[0])
        clue_columns.append(cell[1])

    for node in range(len(shapes[current_n - 1])):
        shape = shapes[current_n - 1][node]
        node_index[depth] = node
        log_progress(depth)

        node_compatible = True
        if (current_n - 1) in chosen:
            if derived_from(chosen[current_n - 1][0], shape, derived_cache) == False:
                node_compatible = False
        if node_compatible == True and (current_n + 1) in chosen:
            if derived_from(shape, chosen[current_n + 1][0], derived_cache) == False:
                node_compatible = False

        if node_compatible == True:
            orientations = get_orientations(current_n, node, shape, orientation_cache)

            seen = set()

            for orientation in orientations:
                rows = []
                columns = []
                for cell in orientation:
                    rows.append(cell[0])
                    columns.append(cell[1])

                row_start = max(clue_rows) - max(rows)
                if row_start < 0:
                    row_start = 0

                row_end = min(clue_rows)
                if row_end > len(board) - max(rows) - 1:
                    row_end = len(board) - max(rows) - 1

                column_start = max(clue_columns) - max(columns)
                if column_start < 0:
                    column_start = 0

                column_end = min(clue_columns)
                if column_end > len(board[0]) - max(columns) - 1:
                    column_end = len(board[0]) - max(columns) - 1

                for row_shift in range(row_start, row_end + 1):
                    for column_shift in range(column_start, column_end + 1):
                        cells = set()
                        for cell in orientation:
                            cells.add((cell[0] + row_shift, cell[1] + column_shift))

                        covers_all_clues = clue_cells[current_n].issubset(cells)
                        if covers_all_clues == False:
                            continue

                        overlaps_blocked = len(cells & blocked_cells[current_n]) > 0
                        if overlaps_blocked == True:
                            continue

                        overlaps_placed = len(cells & occupied) > 0
                        if overlaps_placed == True:
                            continue

                        cells_key = frozenset(cells)
                        if cells_key in seen:
                            continue
                        seen.add(cells_key)

                        transpositions = transpositions + 1
                        log_progress(depth)

                        new_chosen = {}
                        for placed_n in chosen:
                            new_chosen[placed_n] = chosen[placed_n]
                        new_chosen[current_n] = [shape, cells]

                        new_occupied = set(occupied)
                        for cell in cells:
                            new_occupied.add(cell)

                        solve(depth + 1, new_occupied, new_chosen)

    node_index[depth] = 0

n = 16
shapes = []
n_values = []
layer_sizes = []

for i in range(1, n+1):
    with open(f"results/early_pruning/{target}/polyominoes_{i}.json") as file:
        nth_shapes = []
        for shape in json.load(file):
            loaded_shapes = []
            for cell in shape:
                loaded_shapes.append((cell[0], cell[1]))
            nth_shapes.append(loaded_shapes)
    shapes.append(nth_shapes)

for i, n in enumerate(shapes):
    n_values.append(i+1)
    layer_sizes.append(len(n))

print("Cached shapes")
print(f"N values: {n_values}")
print(f"Layer sizes: {layer_sizes}")

#print(len(shapes[3]))

#for i in shapes[3]:
#    print(i)
#    print("-------------------")
#print(len(shapes))

item_removed = True

while item_removed == True:
    item_removed = False
    for i in range(len(shapes) - 1):
        kept_shapes = check_upwards(shapes[i], shapes[i+1])
        if len(kept_shapes) < len(shapes[i]):
            item_removed = True
            shapes[i] = kept_shapes

        kept_shapes = check_downwards(shapes[i], shapes[i+1])
        if len(kept_shapes) < len(shapes[i+1]):
            item_removed = True
            shapes[i+1] = kept_shapes

shrunk_layer_sizes = []

for i in shapes:
    shrunk_layer_sizes.append(len(i))

print("\nShrunken set")
print(f"N values: {n_values}")
print(f"Layer sizes: {shrunk_layer_sizes}")

sorted_branches = []

for i in range(len(n_values)):
    sorted_branches.append([n_values[i], shrunk_layer_sizes[i], shapes[i]])

sorted_branches.sort(key=lambda x: x[1])

#print(sorted_branches)

board = load_board(board_file)

clue_cells = {}
blocked_cells = {}

for branch in sorted_branches:
    constrained_board = board_constraints(board, branch[0])

    clue_cells[branch[0]] = set()
    blocked_cells[branch[0]] = set()
    for row in range(len(constrained_board)):
        for column in range(len(constrained_board[0])):
            if constrained_board[row][column] == "X":
                blocked_cells[branch[0]].add((row, column))
            elif constrained_board[row][column] != "0":
                clue_cells[branch[0]].add((row, column))

search_order = []
for branch in sorted_branches:
    search_order.append(branch[0])

total_branches = 1
for branch in sorted_branches:
    total_branches = total_branches * branch[1]

print("Sorted branches")
print(f"\nSearch order: {search_order}")
print(f"Total branches: {total_branches}")

layer_sizes_in_order = []
for n_value in search_order:
    layer_sizes_in_order.append(len(shapes[n_value - 1]))

#path counting
paths_below = [1] * len(search_order)
for depth in range(len(search_order)):
    for deeper_depth in range(depth + 1, len(search_order)):
        paths_below[depth] = paths_below[depth] * layer_sizes_in_order[deeper_depth]

node_index = [0] * len(search_order)

#seen caches
orientation_cache = {}
derived_cache = {}

#progress tracking
run_percentage = -1
transpositions = 0
last_logged_transpositions = 0

solution = None

solve(0, set(), {})

if solution != None:
    grid = []
    for row in range(len(board)):
        grid.append([0] * len(board[0]))
    for n_value in solution:
        for cell in solution[n_value][1]:
            grid[cell[0]][cell[1]] = n_value
    print("\nsolved grid:")
    for row in grid:
        print(row)
else:
    print("no solution found")

