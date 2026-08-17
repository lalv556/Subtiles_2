import tracemalloc
import os
import sys

#the generators live in the project root so make it importable
sys.path.append(".")

from generators import array_generator
from generators import set_generator
from generators import memory_efficient_generator

def memory_analysis():
    #use tracemalloc to get peak memory usage throughout generator usage
    tracemalloc.start()
    _ = generator.returnShapes(n, use_saved)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{n}: {peak/1000000:.3e} MB")

n = 13
n_from = 1
generator = set_generator
use_saved = False
iterator = True

#streaming needs the previous files to exist, build any missing ones before measuring
if generator == memory_efficient_generator and memory_efficient_generator.jsonl_reader:
    for k in range(1, n):
        if os.path.exists(f"results/memory_efficient/polyominoes_{k}.jsonl") == False:
            if memory_efficient_generator.jsonl_writer and k > 2:
                #the writer saves its own file as it generates
                generator.returnShapes(k)
            else:
                generator.save_shapes(generator.returnShapes(k), k)

if iterator:
    for i in range(n_from, n+1):
        n = i
        memory_analysis()
else:
    memory_analysis()

"""
Array generator
1: 8.000e-05 MB
2: 3.200e-05 MB
3: 2.936e-03 MB
4: 2.968e-03 MB
5: 7.632e-03 MB
6: 2.127e-02 MB
7: 8.847e-02 MB
8: 3.340e-01 MB
9: 1.428e+00 MB

Set generator
1: 2.240e-04 MB
2: 2.240e-04 MB
3: 3.560e-03 MB
4: 7.024e-03 MB
5: 2.126e-02 MB
6: 6.558e-02 MB
7: 2.090e-01 MB
8: 7.463e-01 MB
9: 3.077e+00 MB
10: 1.178e+01 MB
11: 4.604e+01 MB
12: 1.808e+02 MB
13: 7.138e+02 MB

Set generator with jsonl read implementation
1: 2.240e-04 MB
2: 2.240e-04 MB
3: 2.693e-01 MB
4: 1.463e-01 MB
5: 1.573e-01 MB
6: 1.928e-01 MB
7: 3.120e-01 MB
8: 7.711e-01 MB
9: 2.733e+00 MB
10: 1.014e+01 MB
11: 3.949e+01 MB
12: 1.558e+02 MB

Set generator with jsonl read + write implementation
1: 2.240e-04 MB
2: 2.240e-04 MB
3: 2.953e-01 MB
4: 2.769e-01 MB
5: 2.790e-01 MB
6: 2.929e-01 MB
7: 3.405e-01 MB
8: 5.042e-01 MB
9: 1.186e+00 MB
10: 3.867e+00 MB
11: 1.503e+01 MB
12: 6.026e+01 MB

Set generator with jsonl read + write + hashing implementation
1: 2.240e-04 MB
2: 2.240e-04 MB
3: 2.951e-01 MB
4: 2.758e-01 MB
5: 2.763e-01 MB
6: 2.814e-01 MB
7: 2.982e-01 MB
8: 3.355e-01 MB
9: 4.849e-01 MB
10: 5.888e-01 MB
11: 1.423e+00 MB
12: 4.649e+00 MB
13: 1.845e+01
"""

