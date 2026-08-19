# Final Solver

Now that we have generators with pruning specific to each problem (see [3 - Problem Specific Pruning](3%20-%20Problem%20Specific%20Pruning.md)), we can use the generated polyominos to solve the final grid.

Some key details we need to keep in mind are that polyomino shapes shouldn't overlap and polyomino shapes of order n+1 need to extend from polyomino order n (can be rotated/reflected).

## Inputs

The solver starts from the pruned cache saved as json files in `results/early_pruning/subtiles_2`. This includes a total of 10,134 polyomino shapes (a much more refined selection compared to the original exponentially growing set).

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|---:|---:|---:|---:|---:|---:|---:|
| cached shapes | 1 | 1 | 2 | 5 | 12 | 31 | 101 | 344 | 451 | 2434 | 6296 | 2 | 28 | 358 | 54 | 14 |

## The End to End Sweep

To further cut this down we can trim the possible candidates through checking that all children have a valid parent and all parents have a valid child. Doing this throughout the chain ensures that every polyomino follows the previously mentioned extension rule. This sweep is run up and down the chain until a sweep finishes without removing any shapes.

Running this for the puzzle cuts down the number of shapes as follows:

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|---:|---:|---:|---:|---:|---:|---:|
| before sweep | 1 | 1 | 2 | 5 | 12 | 31 | 101 | 344 | 451 | 2434 | 6296 | 2 | 28 | 358 | 54 | 14 |
| after sweep | 1 | 1 | 2 | 3 | 4 | 6 | 5 | 4 | 3 | 3 | 2 | 2 | 11 | 19 | 14 | 14 |

The previous 10,134 shapes have been cut down to 94 (a 99.1% decrease) largely due to the earlier pruning work cutting down the shapes based on board constraints. This pruning work left only two 12th order shapes greatly cutting down the number of possible parents and children across the chain.

## The Tree

The remaining shapes are then sorted by the number of elements at each order of n so they can be treated like a tree, stacked so that the orders with the fewest shapes are placed first and wrong choices are caught with the least work built on top of them.

A full path down the tree picks one shape for every order of n, giving 4,247,147,520 possible paths in total. This number is used to track the percentage through the tree the solver has worked through.

```
search order: 1, 2, 3, 11, 12, 4, 9, 10, 5, 8, 7, 6, 13, 15, 16, 14
layer sizes:  1, 1, 2, 2 , 2 , 3, 3, 3 , 4, 4, 5, 6, 11, 14, 14, 19
total paths:  4,247,147,520
```

## The Search

The tree traversal is in order (depth first) and immediately checks whether shapes of the order one above or below it are already present on the grid. If these are present it is checked whether the shape node is a valid parent or child of these existing shapes. If these adjacent orders haven't been placed yet these checks run after they are included.

After checking for valid extension against existing shapes, at each node the shape is rotated and mirrored to get its 8 orientations and then it is translated until it finds a valid position within the grid. The rules for a shape having a valid position are that it covers all the clue numbers on the grid for it and it doesn't overlap with any other placed shapes or numbers.

If any of these conditions are not met the node is discarded and counted as traversed (including all child nodes).

When a valid position is found the shape is placed on the grid and the solver moves down to the next node of the tree. If no valid positions are found for a node's children the node continues the search from its remaining valid positions and orientations. If none of these have valid positions down the whole tree the node is then discarded.

At each iteration each level of the tree knows how many of its nodes it has already moved past, and by multiplying each of these by the number of paths that run beneath a single node at that level, then adding these together we get the total paths that have been covered so far. This is used to then compute a traversal percentage by taking explored paths/total paths (for the subtiles 2 puzzle the total paths are 4,247,147,520). Since the percentage can pause for long periods of time while a deep part of the tree is being explored the console also prints the number of transpositions tried and the current depth in the tree to show the solver is still working despite a stalled percentage figure.

## The Result

The full solve tried 1,106,537 transpositions and traversed 99.54% of the tree before finding the final solution. On my local machine this took around 2 minutes.

The solved grid:

```
 0  5  5  5 15 15  0 11  0  0  0  0  0
 0  0  0  5  0 15  0 11  0  0 11 11 11
15 15 15  5  0 15 15 11 11 11 11  0 11
15 16 15 15 15 15  8  8  8 12 12 12 11
15 16  0  0  8  8  8  0  8 12  6  6  6
15 16  0 16 16 16 16  0  8 12 12  0  6
 0 16 16 16  3  3 16 16  1  4 12  6  6
13 13 13 13 14  3 16  4  4  4 12 10 10
 7  7  7 13 14 16 16 12 12 12 12 10  0
 7  2  2 13 14 16 14 14 14 14  0 10  0
 7  7 13 13 14 14 14  0  9 14 14 10 10
 0  7 13  9  9  9  9  0  9 14  0  0 10
 0  0 13 13 13 13  9  9  9 14 10 10 10
```

This matches the [solution verified by Jane Street themselves](https://www.janestreet.com/puzzles/subtiles-2-solution/).

To run this solver yourself just run the file in `solver.py` as long as `results/early_pruning/subtiles_2/polyominoes_1-16.json` and `boards/subtiles_2.txt` are populated.
