import numpy
import matplotlib.pyplot as plt

#runtimes from run_evaluator.py
n_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
array_runtimes = [1.431e-06, 9.537e-06, 2.403e-04, 1.391e-03, 1.042e-02, 9.278e-02, 8.523e-01, 1.028e+01, 2.246e+02]
set_runtimes = [1.907e-06, 2.384e-06, 1.318e-04, 3.777e-04, 1.489e-03, 5.111e-03, 2.070e-02, 7.458e-02, 2.944e-01]

def fit_line(n_values, runtimes):
    #fit a straight line against exponentially growing values
    slope, intercept = numpy.polyfit(n_values, numpy.log10(runtimes), 1)
    return slope, intercept

def predicted_runtimes(slope, intercept, up_to):
    #evaluate the fitted line for every n from 1 up to up_to
    predictions = []
    for n in range(1, up_to + 1):
        predictions.append(10 ** (slope * n + intercept))
    return predictions

def print_predictions(predictions, n_values):
    #print the predictions for the values we have no measurement for
    for n in range(len(n_values) + 1, len(predictions) + 1):
        print(f"n={n}: predicted {predictions[n-1]:.3e} seconds")

def draw_graph(n_values, runtimes, predictions, slope, title, name="measured"):
    fit_n = list(range(1, len(predictions) + 1))
    plt.plot(n_values, runtimes, marker="o", linestyle="", label=name)
    plt.plot(fit_n, predictions, linestyle="--", label=f"{name} slope: {10 ** slope:.2f}x per n step")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("runtime (seconds)")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

def plot_data(up_to):
    slope, intercept = fit_line(n_values, array_runtimes)
    print(f"array slope is: {slope:.2f} meaning runtime grows {10**slope:.2f}x at each iteration")
    predictions = predicted_runtimes(slope, intercept, up_to)
    draw_graph(n_values, array_runtimes, predictions, slope, "generator runtime as n increases", "array")

def extrapolate(up_to):
    slope, intercept = fit_line(n_values, array_runtimes)
    predictions = predicted_runtimes(slope, intercept, up_to)
    print_predictions(predictions, n_values)

    #show the predicted points past the measurements in their own colour
    extrapolated_n = []
    extrapolated_runtimes = []
    for n in range(len(n_values) + 1, up_to + 1):
        extrapolated_n.append(n)
        extrapolated_runtimes.append(predictions[n-1])
    plt.plot(extrapolated_n, extrapolated_runtimes, marker="o", linestyle="", color="tab:red", label="array extrapolated")

def compare(up_to):
    #add the set generator to the graph with its own best fit line
    set_slope, set_intercept = fit_line(n_values, set_runtimes)
    set_predictions = predicted_runtimes(set_slope, set_intercept, up_to)
    print(f"set slope is: {set_slope:.2f} meaning runtime grows {10**set_slope:.2f}x at each iteration")

    fit_n = list(range(1, up_to + 1))
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

comparison = True
extrapolation = True
extrapolate_to = 17

if extrapolation:
    up_to = extrapolate_to
else:
    up_to = len(n_values)

if comparison:
    compare(up_to)
if extrapolation:
    extrapolate(up_to)
plot_data(up_to)
