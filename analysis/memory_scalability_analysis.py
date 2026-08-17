import numpy
import matplotlib.pyplot as plt

#memory usage from evaluators/memory_evaluator.py
n_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
array_generator_memory = [8.000e-05, 3.200e-05, 2.936e-03, 2.968e-03, 7.632e-03, 2.127e-02, 8.847e-02, 3.340e-01, 1.428e+00]
set_generator_memory = [2.240e-04, 2.240e-04, 3.048e-03, 6.704e-03, 2.109e-02, 6.558e-02, 2.090e-01, 7.463e-01, 3.077e+00, 1.178e+01, 4.604e+01, 1.808e+02, 7.138e+02]
memory_efficient_generator_memory = [2.240e-04, 2.240e-04, 2.951e-01, 2.758e-01, 2.763e-01, 2.814e-01, 2.982e-01, 3.355e-01, 4.849e-01, 5.888e-01, 1.423e+00, 4.649e+00, 1.845e+01]

#the growth rate only settles at bigger n so fit from there
fit_from = 7
#the memory efficient generator sits on a flat file overhead floor which only fully clears by n=12 so fit later
memory_efficient_fit_from = 12

comparison = True
array_analysis = False
extrapolation = True
extrapolate_to = 17

if extrapolation:
    up_to = extrapolate_to
else:
    up_to = len(n_values)

fit_n = []
for i in range(1, up_to + 1):
    fit_n.append(i)

#add the set generator results to the graph
if comparison:
    set_slope, set_intercept = numpy.polyfit(n_values[fit_from-1:], numpy.log10(set_generator_memory[fit_from-1:]), 1)
    print(f"set slope is: {set_slope:.2f} meaning memory grows {10**set_slope:.2f}x at each iteration")

    set_predictions = []
    for n in range(1, up_to + 1):
        set_predictions.append(10 ** (set_slope * n + set_intercept))

    plt.plot(n_values, set_generator_memory, marker="o", linestyle="", color="tab:green", label="set")
    plt.plot(fit_n, set_predictions, linestyle="--", color="tab:green", label=f"set slope: {10 ** set_slope:.2f}x per n step")

    if extrapolation:
        #show the predicted points past the measurements in their own colour
        extrapolated_n = []
        extrapolated_runtimes = []
        for n in range(len(n_values) + 1, up_to + 1):
            extrapolated_n.append(n)
            extrapolated_runtimes.append(set_predictions[n-1])
        plt.plot(extrapolated_n, extrapolated_runtimes, marker="o", linestyle="", color="tab:purple", label="set extrapolated")

#add the memory efficient generator results to the graph
if comparison:
    memory_efficient_slope, memory_efficient_intercept = numpy.polyfit(n_values[memory_efficient_fit_from-1:], numpy.log10(memory_efficient_generator_memory[memory_efficient_fit_from-1:]), 1)
    print(f"memory efficient slope is: {memory_efficient_slope:.2f} meaning memory grows {10**memory_efficient_slope:.2f}x at each iteration")

    memory_efficient_predictions = []
    for n in range(1, up_to + 1):
        memory_efficient_predictions.append(10 ** (memory_efficient_slope * n + memory_efficient_intercept))

    plt.plot(n_values, memory_efficient_generator_memory, marker="o", linestyle="", color="tab:cyan", label="memory efficient")
    plt.plot(fit_n, memory_efficient_predictions, linestyle="--", color="tab:cyan", label=f"memory efficient slope: {10 ** memory_efficient_slope:.2f}x per n step")

    if extrapolation:
        #show the predicted points past the measurements in their own colour
        extrapolated_n = []
        extrapolated_runtimes = []
        for n in range(len(n_values) + 1, up_to + 1):
            extrapolated_n.append(n)
            extrapolated_runtimes.append(memory_efficient_predictions[n-1])
        plt.plot(extrapolated_n, extrapolated_runtimes, marker="o", linestyle="", color="tab:olive", label="memory efficient extrapolated")

#the array generator and its line of best fit
if array_analysis:
    #the array generator was only measured up to n=9
    array_n = n_values[:len(array_generator_memory)]
    array_slope, array_intercept = numpy.polyfit(array_n[fit_from-1:], numpy.log10(array_generator_memory[fit_from-1:]), 1)
    print(f"array slope is: {array_slope:.2f} meaning memory grows {10**array_slope:.2f}x at each iteration")

    array_predictions = []
    for n in range(1, up_to + 1):
        array_predictions.append(10 ** (array_slope * n + array_intercept))

    if extrapolation:
        for n in range(len(array_generator_memory) + 1, up_to + 1):
            print(f"n={n}: predicted {array_predictions[n-1]:.3e} MB")

        #extrapolated points have a unique colour
        extrapolated_n = []
        extrapolated_runtimes = []
        for n in range(len(array_generator_memory) + 1, up_to + 1):
            extrapolated_n.append(n)
            extrapolated_runtimes.append(array_predictions[n-1])
        plt.plot(extrapolated_n, extrapolated_runtimes, marker="o", linestyle="", color="tab:red", label="array extrapolated")

    plt.plot(array_n, array_generator_memory, marker="o", linestyle="", label="array")
    plt.plot(fit_n, array_predictions, linestyle="--", label=f"array slope: {10 ** array_slope:.2f}x per n step")
plt.yscale("log")
plt.xlabel("n")
plt.ylabel("peak memory (MB)")
plt.title("generator memory usage as n increases")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
