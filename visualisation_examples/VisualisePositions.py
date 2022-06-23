import pickle
import numpy as np
import scipy.signal
from math import sin, cos, pi
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap


def get_position_density(x_coord, y_coord, rel_robot_rad, normalisation_fact):
    """
    Computes the density map as a 2d histogram of the points defined by x_coord, y_coord to which 
    is applied a convolution with a circular kernel of radius rel_robot_rad. This is normalised by 
    normalisation_fact.
    """
    y_r,x_r = np.ogrid[-rel_robot_rad: rel_robot_rad+1, -rel_robot_rad: rel_robot_rad+1]
    mask = x_r**2+y_r**2 <= rel_robot_rad**2

    H, xedges, yedges = np.histogram2d(x_coord, y_coord, bins=resolution, range=edges)

    H_p = scipy.signal.convolve2d(H.T, mask, mode="same")/normalisation_fact

    return H_p, xedges, yedges


resolution = 1000                                   # resolution of the plot, is the same as the number of bins in a 2d histogram
edges = [[-1.5, 1.5], [-1.5, 1.5]]                   
robot_radius = 0.035
relative_rad = round(robot_radius/3*resolution)     # relative radius in as a number of bins 

data_step_size = 5                                  # sapling of the positions

# defines custom color map so that the value 0 is transparent

cmap = plt.cm.get_cmap("cool")
my_cmap = cmap(np.arange(cmap.N))
my_cmap[0,-1] = 0
my_cmap = ListedColormap(my_cmap)

# sets the arena box which is a dodecagon

dodecagon_coords = []

radius = 1.231/cos(pi/12)
for i in range(12):
    angle = pi/6*i+pi/12
    dodecagon_coords.append([radius*cos(angle), radius*sin(angle)])

p1 = plt.Polygon(dodecagon_coords, edgecolor = 'k', fill=False, lw=2)
p2 = plt.Polygon(dodecagon_coords, edgecolor = 'k', fill=False, lw=2)


with open("../Experiment/results/benchamrk_results.pkl", "rb") as f:
    d = pickle.load(f)

position = d["Position"]["chocolate"][0]

normalisation_fact = len(position["epuck0"]["x"])/data_step_size      

fig, axes = plt.subplots(1,2)

(ax1, ax2) = axes

x1 = []
y1 = []
for robot in position.values():
    x1 += robot["x"][::data_step_size]
    y1 += robot["y"][::data_step_size]

x1 = np.array(x1)
y1 = np.array(y1)

x2 = []
y2 = []
for robot in d["Position"]["evoStick"][0].values():
    x2 += robot["x"][::data_step_size]
    y2 += robot["y"][::data_step_size]

x2 = np.array(x2)
y2 = np.array(y2)

# calculates the density map for the chocolate experiment
dens_map1, xedges, yedges = get_position_density(x1, y1, relative_rad, normalisation_fact)
# calculates the density map for the evoStick experiment
dens_map2, xedges, yedges = get_position_density(x2, y2, relative_rad, normalisation_fact)

ax1.set_facecolor("lightgrey")
ax2.set_facecolor("lightgrey")
ax1.add_patch(p1)
ax2.add_patch(p2)

# calculetes the limits of the color map so that the colorbar has the same meaning for both maps
max_value = np.max([dens_map1, dens_map2])
min_value = np.min([dens_map1, dens_map2])

# plots the histograms
im1 = ax1.imshow(dens_map1, origin='lower', interpolation="gaussian",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], cmap=my_cmap, zorder=2, vmax=max_value, vmin=min_value)
im2 = ax2.imshow(dens_map2, origin='lower', interpolation="gaussian",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], cmap=my_cmap, zorder=2, vmax=max_value, vmin=min_value)


# sets the font sizes and labels
ax1.tick_params(axis='y', labelsize=18)
ax1.tick_params(axis='x', labelsize=18)
ax2.tick_params(axis='y', labelsize=18)
ax2.tick_params(axis='x', labelsize=18)

ax1.set_xlabel("chocolate", fontsize=18)
ax2.set_xlabel("evoStick", fontsize=18)

# adds the colorbar
cbar = fig.colorbar(im1,orientation="horizontal",ax=axes.ravel().tolist())
cbar.ax.tick_params(labelsize=18)

plt.show()

