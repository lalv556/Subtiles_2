import tracemalloc

import array_generator
import set_generator

def memory_analysis():
    #use tracemalloc to get peak memory usage throughout generator usage
    tracemalloc.start()
    _ = generator.returnShapes(n, use_saved)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{n}: {peak/1000000:.3e} MB")

n = 9
generator = array_generator
use_saved = False
iterator = True

if iterator:
    for i in range(1, n+1):
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
3: 3.048e-03 MB
4: 6.704e-03 MB
5: 2.109e-02 MB
6: 6.558e-02 MB
7: 2.090e-01 MB
8: 7.463e-01 MB
9: 3.077e+00 MB
"""