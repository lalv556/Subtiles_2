#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict, deque
from functools import lru_cache
from typing import Dict, FrozenSet, Iterable, List, Optional, Set, Tuple
import time

Cell = Tuple[int, int]
Shape = FrozenSet[Cell]  # absolute board coords

# ---- your grid (0 = unknown) ----
subtiles2 = [
    [0 ,  0,  0,  0, 15,  0,  0,  0,  0,  0,  0,  0,  0],
    [0 ,  0,  0,  0,  0,  0,  0, 11,  0,  0,  0,  0,  0],
    [0 , 15,  0,  5,  0,  0, 15,  0, 11,  0, 11,  0,  0],
    [0 ,  0,  0,  0, 15,  0,  0,  8,  0, 12,  0, 12,  0],
    [0 , 16,  0,  0,  0,  8,  0,  0,  0,  0,  6,  0,  0],
    [0 ,  0,  0, 16,  0,  0,  0,  0,  0,  0,  0,  0,  6],
    [0 ,  0, 16,  0,  3,  0, 16,  0,  1,  0, 12,  0,  0],
    [13,  0,  0,  0,  0,  0,  0,  0,  0,  4,  0,  0,  0],
    [0 ,  0,  7,  0,  0,  0,  0,  12,  0,  0,  0, 10,  0],
    [0 ,  2,  0, 13,  0, 16,  0,  0, 14,  0,  0,  0,  0],
    [0 ,  0, 13,  0, 14,  0, 14,  0,  0, 14,  0, 10,  0],
    [0 ,  0,  0,  0,  0,  9,  0,  0,  0,  0,  0,  0,  0],
    [0 ,  0,  0,  0,  0,  0,  0,  0,  9,  0,  0,  0,  0],
]

R, C = 13, 13

def nbrs(cell: Cell) -> Iterable[Cell]:
    r, c = cell
    if r > 0: yield (r - 1, c)
    if r + 1 < R: yield (r + 1, c)
    if c > 0: yield (r, c - 1)
    if c + 1 < C: yield (r, c + 1)

def connected(cells: Set[Cell]) -> bool:
    if not cells:
        return False
    q = deque([next(iter(cells))])
    seen = {q[0]}
    while q:
        u = q.popleft()
        for v in nbrs(u):
            if v in cells and v not in seen:
                seen.add(v)
                q.append(v)
    return len(seen) == len(cells)

def norm(rel: Iterable[Tuple[int, int]]) -> FrozenSet[Tuple[int, int]]:
    pts = list(rel)
    minr = min(r for r, _ in pts)
    minc = min(c for _, c in pts)
    return frozenset((r - minr, c - minc) for r, c in pts)

def shape_to_rel(S: Shape) -> FrozenSet[Tuple[int, int]]:
    return norm(S)

def rel_transforms(rel: FrozenSet[Tuple[int, int]]) -> Set[FrozenSet[Tuple[int, int]]]:
    pts = list(rel)
    out: Set[FrozenSet[Tuple[int, int]]] = set()
    for refl in (0, 1):
        for rot in range(4):
            t = []
            for r, c in pts:
                x, y = r, c
                if refl:
                    y = -y
                for _ in range(rot):
                    x, y = y, -x
                t.append((x, y))
            out.add(norm(t))
    return out

def contains_shape(outer: Shape, inner: Shape) -> bool:
    outer_set = set(outer)
    inner_rel = shape_to_rel(inner)
    for tr in rel_transforms(inner_rel):
        maxr = max(r for r, _ in tr)
        maxc = max(c for _, c in tr)
        for br in range(R - maxr):
            for bc in range(C - maxc):
                placed = {(br + r, bc + c) for r, c in tr}
                if placed.issubset(outer_set):
                    return True
    return False

# forced clue cells: value -> set of coordinates
forced: Dict[int, Set[Cell]] = defaultdict(set)
for r in range(R):
    for c in range(C):
        v = subtiles2[r][c]
        if v:
            forced[v].add((r, c))

N = max(forced)  # assumes N is the largest given clue value

def ascii_board(sol: Dict[int, Shape], upto: int, clues_grid: Optional[List[List[int]]] = None) -> str:
    grid = [[" ." for _ in range(C)] for _ in range(R)]
    for k in range(1, upto + 1):
        if k not in sol:
            continue
        for r, c in sol[k]:
            grid[r][c] = f"{k:2d}"

    # Overlay original clues with a marker: "d*" where d is the tens digit (keeps width 2)
    if clues_grid is not None:
        for r in range(R):
            for c in range(C):
                v = clues_grid[r][c]
                if v:
                    s = f"{v:2d}"
                    grid[r][c] = s[0] + "*"
    return "\n".join(" ".join(row) for row in grid)

class Progress:
    def __init__(self, every_nodes: int = 2000, every_seconds: float = 2.0, show_board: bool = True):
        self.every_nodes = every_nodes
        self.every_seconds = every_seconds
        self.show_board = show_board
        self.nodes = 0
        self.pruned = 0
        self.start = time.time()
        self.last_t = self.start
        self.last_nodes = 0

    def tick(self, msg: str, sol: Dict[int, Shape], grid=None):
        self.nodes += 1
        now = time.time()
        if (self.nodes % self.every_nodes == 0) or (now - self.last_t >= self.every_seconds):
            dt = now - self.last_t
            dnodes = self.nodes - self.last_nodes
            rate = dnodes / dt if dt > 0 else 0.0
            elapsed = now - self.start
            depth = max(sol.keys(), default=0)
            print(f"[t={elapsed:7.1f}s] {msg}  placed_up_to={depth:2d}  nodes={self.nodes:,}  rate={rate:,.0f}/s  pruned={self.pruned:,}",
                  flush=True)
            if self.show_board:
                print(ascii_board(sol, upto=depth, clues_grid=grid))
                print("-" * 80, flush=True)
            self.last_t = now
            self.last_nodes = self.nodes

@lru_cache(None)
def connected_supersets_size_k_from_must(k: int, must: Tuple[Cell, ...]) -> Tuple[Shape, ...]:
    """
    Enumerate connected sets of size k containing all 'must' cells.
    Cached, but returned as a tuple so it can be cached safely.
    """
    must_set = set(must)
    if len(must_set) > k:
        return tuple()
    if k == len(must_set):
        return (frozenset(must_set),) if connected(must_set) else tuple()

    start = frozenset(must_set)
    seen = {start}
    stack = [start]
    res: List[Shape] = []
    while stack:
        S = stack.pop()
        if len(S) == k:
            if connected(set(S)):
                res.append(S)
            continue
        boundary = set()
        for cell in S:
            for nb in nbrs(cell):
                if nb not in S:
                    boundary.add(nb)
        for nb in boundary:
            T = frozenset(set(S) | {nb})
            if T not in seen:
                seen.add(T)
                stack.append(T)

    return tuple(res)

def solve(show_progress: bool = True) -> Optional[Dict[int, Shape]]:
    prog = Progress(every_nodes=1000, every_seconds=1.5, show_board=show_progress)
    sol: Dict[int, Shape] = {}

    # k=1 must be exactly the forced single cell (in your grid it is)
    must1 = tuple(sorted(forced.get(1, set())))
    c1 = connected_supersets_size_k_from_must(1, must1)
    if not c1:
        return None

    def rec(k: int) -> bool:
        if k > N:
            return True

        must = tuple(sorted(forced.get(k, set())))
        prog.tick(f"Enumerating/trying K={k:2d}", sol, grid=subtiles2)

        # Generate candidates for this K
        cands = connected_supersets_size_k_from_must(k, must)
        if not cands:
            return False

        if k == 1:
            for S in cands:
                sol[1] = S
                if rec(2):
                    return True
                del sol[1]
            return False

        prev = sol[k - 1]

        # Filter by containment; tick during filtering so you see life even if huge
        kept: List[Shape] = []
        for idx, S in enumerate(cands):
            if contains_shape(S, prev):
                kept.append(S)
            else:
                prog.pruned += 1
            if idx % 5000 == 0 and idx > 0:
                prog.tick(f"Filtering K={k:2d} ({idx:,}/{len(cands):,}) kept={len(kept):,}", sol, grid=subtiles2)

        prog.tick(f"Backtracking K={k:2d} kept={len(kept):,}/{len(cands):,}", sol, grid=subtiles2)

        for j, S in enumerate(kept):
            sol[k] = S
            if j % 2000 == 0 and j > 0:
                prog.tick(f"Trying K={k:2d} candidate {j:,}/{len(kept):,}", sol, grid=subtiles2)
            if rec(k + 1):
                return True
            del sol[k]

        return False

    # Seed k=1 first so placed_up_to is nonzero quickly
    sol[1] = c1[0]
    if rec(2):
        return sol
    return None

def render(sol: Dict[int, Shape]) -> List[List[int]]:
    out = [[0] * C for _ in range(R)]
    for k, S in sol.items():
        for r, c in S:
            out[r][c] = k
    return out

def main() -> None:
    print(f"Grid {R}x{C}, assumed N={N}, forced counts: " +
          ", ".join(f"{k}:{len(v)}" for k, v in sorted(forced.items())),
          flush=True)

    sol = solve(show_progress=True)
    if sol is None:
        print("No solution found for N =", N, flush=True)
        return

    filled = render(sol)
    print("\nSolved grid:\n", flush=True)
    for row in filled:
        print(" ".join(f"{v:2d}" for v in row))

if __name__ == "__main__":
    main()
