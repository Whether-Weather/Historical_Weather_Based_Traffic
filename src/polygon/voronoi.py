import matplotlib.pyplot as pl
import numpy as np
import scipy as sp
import scipy.spatial
import sys

eps = sys.float_info.epsilon

n_towers = 100
towers = np.random.rand(n_towers, 2)
bounding_box = np.array([0., 1., 0., 1.]) # [x_min, x_max, y_min, y_max]

def in_box(towers, bounding_box):
    x = bounding_box[0]
    y = towers[:, 0]
    z = bounding_box[1]
    a = bounding_box[2]
    b = towers[:, 1]
    c = bounding_box[3]

    return np.logical_and(np.logical_and(bounding_box[0] <= towers[:, 0],
                                         towers[:, 0] <= bounding_box[1]),
                          np.logical_and(bounding_box[2] <= towers[:, 1],
                                         towers[:, 1] <= bounding_box[3]))


def voronoi(towers, bounding_box):
    # Select towers inside the bounding box
    i = in_box(towers, bounding_box)
    # Mirror points
    points_center = towers[i, :]
    points_left = np.copy(points_center)
    points_left[:, 0] = bounding_box[0] - (points_left[:, 0] - bounding_box[0])
    points_right = np.copy(points_center)
    points_right[:, 0] = bounding_box[1] + (bounding_box[1] - points_right[:, 0])
    points_down = np.copy(points_center)
    points_down[:, 1] = bounding_box[2] - (points_down[:, 1] - bounding_box[2])
    points_up = np.copy(points_center)
    points_up[:, 1] = bounding_box[3] + (bounding_box[3] - points_up[:, 1])
    points = np.append(points_center,
                       np.append(np.append(points_left,
                                           points_right,
                                           axis=0),
                                 np.append(points_down,
                                           points_up,
                                           axis=0),
                                 axis=0),
                       axis=0)
    # Compute Voronoi
    vor = sp.spatial.Voronoi(points)
    # Filter regions
    regions = []
    for region in vor.regions:
        flag = True
        for index in region:
            if index == -1:
                flag = False
                break
            else:
                x = vor.vertices[index, 0]
                y = vor.vertices[index, 1]
                if not(bounding_box[0] - eps <= x and x <= bounding_box[1] + eps and
                       bounding_box[2] - eps <= y and y <= bounding_box[3] + eps):
                    flag = False
                    break
        if region != [] and flag:
            regions.append(region)
    vor.filtered_points = points_center
    vor.filtered_regions = regions
    return vor

def centroid_region(vertices):
    # Polygon's signed area
    A = 0
    # Centroid's x
    C_x = 0
    # Centroid's y
    C_y = 0
    for i in range(0, len(vertices) - 1):
        s = (vertices[i, 0] * vertices[i + 1, 1] - vertices[i + 1, 0] * vertices[i, 1])
        A = A + s
        C_x = C_x + (vertices[i, 0] + vertices[i + 1, 0]) * s
        C_y = C_y + (vertices[i, 1] + vertices[i + 1, 1]) * s
    A = 0.5 * A
    C_x = (1.0 / (6.0 * A)) * C_x
    C_y = (1.0 / (6.0 * A)) * C_y
    return np.array([[C_x, C_y]])

def vor_draw(draw_towers, draw_bounding_box):
    vor = voronoi(draw_towers, draw_bounding_box)
    x = len(draw_towers)
    np_list = draw_towers.tolist()
    fig = pl.figure()
    ax = fig.gca()
    # Plot initial points
    ax.plot(vor.filtered_points[:, 0], vor.filtered_points[:, 1], 'b.')
    ret_polygons = {}
    # Plot ridges points
    for i, region in enumerate(vor.filtered_regions):
        y = len(vor.filtered_regions)
        z = np_list[i]
        vertices = vor.vertices[region, :]
        holder = []
        for element in vertices:
            holder.append([element[1], element[0]])
        holder.append([vertices[0][1], vertices[0][0]])
        key_string = str(np_list[i][1]) + "," + str(np_list[i][0])
        ret_polygons[key_string] = holder

        ax.plot(vertices[:, 0], vertices[:, 1], 'go')
    # Plot ridges
    for region in vor.filtered_regions:
        vertices = vor.vertices[region + [region[0]], :]
        ax.plot(vertices[:, 0], vertices[:, 1], 'k-')
    # Compute and plot centroids
    centroids = []
    for region in vor.filtered_regions:
        vertices = vor.vertices[region + [region[0]], :]
        centroid = centroid_region(vertices)
        centroids.append(list(centroid[0, :]))
        ax.plot(centroid[:, 0], centroid[:, 1], 'r.')

    #[45.266, 49.084, -124.993, -116.719]
    # ax.set_xlim([-0.1, 1.1])
    # ax.set_ylim([-0.1, 1.1])
    ax.set_xlim([45, 49.2])
    ax.set_ylim([-125.2, -116.5])
    pl.savefig("test_bounded_voronoi.png")

    sp.spatial.voronoi_plot_2d(vor)
    pl.savefig("test_voronoi.png")
    return ret_polygons

if __name__ == '__main__':
    print("call function")