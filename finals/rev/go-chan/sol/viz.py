from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

n = 4

path = [[0,0,0], [0,0,1], [1,0,1], [1,0,0], [1,1,0], [1,1,1], [0,1,1], [0,1,0]]
path = [[0, 0, 0], [1, 0, 0], [1, 0, 1], [2, 0, 1], [3, 0, 1], [3, 1, 1], [2, 1, 1], [2, 1, 0], [2, 0, 0], [3, 0, 0], [3, 1, 0], [3, 2, 0], [3, 2, 1], [2, 2, 1], [2, 3, 1], [2, 3, 0], [3, 3, 0], [3, 3, 1], [3, 3, 2], [2, 3, 2], [2, 3, 3], (3, 3, 3)]
# grid = [
#     [
#         [
#             ["Left","Right"],
#             ["Left", "Back"]
#         ],
#         [
#             ["Right","Left"],
#             ["Left", "Back"]
#         ]
#     ],
#     [
#         [
#             ["Right","Bottom"],
#             ["Front", "Left"]
#         ],
#         [
#             ["Front","Right"],
#             ["Back", "Left"]
#         ]
#     ]
# ]
import json
grid = json.load(open("../src/out.json"))

datasets = []
for i in range(n):
    for j in range(n):
        for k in range(n):
            for face in grid[i][j][k]:
                if face == "Top":
                    datasets.append({"x":[k, k], "y": [i, i], "z": [-j, -j+0.5], "colour":"red"})
                elif face == "Bottom":
                    datasets.append({"x":[k, k], "y": [i, i], "z": [-j, -j-0.5], "colour":"red"})
                elif face == "Right":
                    datasets.append({"x":[k, k+0.5], "y": [i, i], "z": [-j, -j], "colour":"red"})
                elif face == "Left":
                    datasets.append({"x":[k, k-0.5], "y": [i, i], "z": [-j, -j], "colour":"red"})
                elif face == "Front":
                    datasets.append({"x":[k, k], "y": [i, i-0.5], "z": [-j, -j], "colour":"red"})
                elif face == "Back":
                    datasets.append({"x":[k, k], "y": [i, i+0.5], "z": [-j, -j], "colour":"red"})
    
# for i in range(n+1):
#     for j in range(n+1):
#         datasets.append({"x":[-0.5+i,-0.5+i], "y": [-0.5+j, -0.5+j], "z": [0.5, -n + 0.5], "colour":"blue"})
#         datasets.append({"y":[-0.5+i,-0.5+i], "z": [-n+0.5+j, -n+0.5+j], "x": [-0.5, n - 0.5], "colour":"blue"})
#         datasets.append({"x":[-0.5+i,-0.5+i], "z": [-n+0.5+j, -n+0.5+j], "y": [-0.5, n - 0.5], "colour":"blue"})


# datasets += [{"x":[x[2] for x in path], "y":[x[0] for x in path], "z":[-x[1] for x in path], "colour": "blue"}]

for dataset in datasets:
    ax.plot(dataset["x"], dataset["y"], dataset["z"], color=dataset["colour"])

ax.set_xticks(np.arange(0, n, 1))
ax.set_yticks(np.arange(0, n, 1))
ax.set_zticks(np.arange(-n,0, 1))
ax.set_zlabel("Top/Down")
ax.set_ylabel("Front/Back")
ax.set_xlabel("Left/Right")

plt.show()