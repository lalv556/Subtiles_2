import sys
import matplotlib.pyplot as plt

#the generators live in the project root so make it importable
sys.path.append(".")

from generators import selective_pruning

#full counts for each n
polyominos_series = [1, 1, 2, 5, 12, 35, 108, 369, 1285, 4655, 17073, 63600, 238591, 901971, 3426576, 13079255, 50107909]

n = 16

n_values = [1]
unpruned_counts = [polyominos_series[0]]

#walk the chain once so every generation only builds off the survivors below it
shapes = selective_pruning.filter_shapes([{(0, 0)}], 1)
pruned_counts = [len(shapes)]
print(f"1: {pruned_counts[-1]} of {unpruned_counts[-1]} shapes survive")

for i in range(2, n+1):
    generated = []
    seen = set()
    for shape in shapes:
        selective_pruning.extend_shape(shape, 0, 0, i, generated, seen)
    shapes = selective_pruning.filter_shapes(generated, i)

    n_values.append(i)
    unpruned_counts.append(polyominos_series[i-1])
    pruned_counts.append(len(shapes))
    print(f"{i}: {pruned_counts[-1]} of {unpruned_counts[-1]} shapes survive")

print(f"total: {sum(pruned_counts)} shapes generated instead of {sum(unpruned_counts)}")

plt.plot(n_values, unpruned_counts, marker="o", linestyle="", color="tab:green", label="unpruned")
plt.plot(n_values, pruned_counts, marker="o", linestyle="", color="tab:cyan", label="pruned")
plt.yscale("log")
plt.xlabel("n")
plt.ylabel("number of polyominoes")
plt.title("unpruned vs pruned generation counts")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
