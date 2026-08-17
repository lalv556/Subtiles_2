import numpy
import matplotlib.pyplot as plt

#runtimes from evaluators/runtime_evaluator.py
n_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
array_runtimes = [1.431e-06, 9.537e-06, 2.403e-04, 1.391e-03, 1.042e-02, 9.278e-02, 8.523e-01, 1.028e+01, 2.246e+02]
set_runtimes = [1.907e-06, 2.384e-06, 1.318e-04, 3.777e-04, 1.489e-03, 5.111e-03, 2.070e-02, 7.458e-02, 2.944e-01]

comparison = True
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
    set_slope, set_intercept = numpy.polyfit(n_values, numpy.log10(set_runtimes), 1)
    print(f"set slope is: {set_slope:.2f} meaning runtime grows {10**set_slope:.2f}x at each iteration")

    set_predictions = []
    for n in range(1, up_to + 1):
        set_predictions.append(10 ** (set_slope * n + set_intercept))

    plt.plot(n_values, set_runtimes, marker="o", linestyle="", color="tab:green", label="set")
    plt.plot(fit_n, set_predictions, linestyle="--", color="tab:green", label=f"set slope: {10 ** set_slope:.2f}x per n step")

    if extrapolation:
        #show the predicted points past the measurements in their own colour
        extrapolated_n = []
        extrapolated_runtimes = []
        for n in range(len(n_values) + 1, up_to + 1):
            extrapolated_n.append(n)
            extrapolated_runtimes.append(set_predictions[n-1])
        plt.plot(extrapolated_n, extrapolated_runtimes, marker="o", linestyle="", color="tab:purple", label="set extrapolated")

#the array generator and its best fit line
array_slope, array_intercept = numpy.polyfit(n_values, numpy.log10(array_runtimes), 1)
print(f"array slope is: {array_slope:.2f} meaning runtime grows {10**array_slope:.2f}x at each iteration")

array_predictions = []
for n in range(1, up_to + 1):
    array_predictions.append(10 ** (array_slope * n + array_intercept))

if extrapolation:
    for n in range(len(n_values) + 1, up_to + 1):
        print(f"n={n}: predicted {array_predictions[n-1]:.3e} seconds")

    #extrapolated points have a unique colour
    extrapolated_n = []
    extrapolated_runtimes = []
    for n in range(len(n_values) + 1, up_to + 1):
        extrapolated_n.append(n)
        extrapolated_runtimes.append(array_predictions[n-1])
    plt.plot(extrapolated_n, extrapolated_runtimes, marker="o", linestyle="", color="tab:red", label="array extrapolated")

plt.plot(n_values, array_runtimes, marker="o", linestyle="", label="array")
plt.plot(fit_n, array_predictions, linestyle="--", label=f"array slope: {10 ** array_slope:.2f}x per n step")
plt.yscale("log")
plt.xlabel("n")
plt.ylabel("runtime (seconds)")
plt.title("generator runtime as n increases")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
