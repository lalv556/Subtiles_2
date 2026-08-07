import cProfile
import time

import array_generator
import set_generator

def time_analysis():
    if per_function_analysis:
        #get results for how long each function ran for
        profiler = cProfile.Profile()
        profiler.run("generator.returnShapes(n, use_saved)")

        function_times = []
        for i in profiler.getstats():
            #print(i)
            function_object = i.code
            #print(function_object)
            if type(function_object) == str:
                function_name = function_object
            else:
                function_name = i.code.co_name
            
            function_times.append([i.inlinetime, function_name])

        sorted_times = sorted(function_times, key=lambda x: x[0])
        sorted_times = sorted_times[-1:-11:-1]
        total_time = 0
        for i in sorted_times:
            total_time += i[0]

        for placement, function_run in enumerate(sorted_times):
            print(f"{placement+1}: {function_run[1]}, Occupancy: {function_run[0]/total_time*100:.2f}%")
    else:
        start = time.time()
        shapes = generator.returnShapes(n, use_saved)
        print(f"{n}: {time.time() - start:.3e} seconds")

n = 9
generator = set_generator
use_saved = False
per_function_analysis = False
iterator = True

if iterator:
    for i in range(1, n+1):
        n = i
        time_analysis()
else:
    time_analysis()

"""
Array generator
1: 1.431e-06 seconds
2: 9.537e-06 seconds
3: 2.403e-04 seconds
4: 1.391e-03 seconds
5: 1.042e-02 seconds
6: 9.278e-02 seconds
7: 8.523e-01 seconds
8: 1.028e+01 seconds
9: 2.246e+02 seconds

Set generator
1: 1.907e-06 seconds
2: 2.384e-06 seconds
3: 1.318e-04 seconds
4: 3.777e-04 seconds
5: 1.489e-03 seconds
6: 5.111e-03 seconds
7: 2.070e-02 seconds
8: 7.458e-02 seconds
9: 2.944e-01 seconds
"""