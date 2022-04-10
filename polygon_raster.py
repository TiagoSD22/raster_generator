import math
import numpy as np
from bresenham import bresenham


class PolygonRaster:
    def raster_equilateral_triangle(self, length):
        v1 = (0, 0)
        v2 = (length, 0)
        v3 = (length // 2, int(length * math.sqrt(3) / 2))

        polygon_vertex_list = [v1, v2, v3]

        print("Equilateral Triangle vertex list: ", polygon_vertex_list)

        edge1 = list(bresenham(v1[0], v1[1], v2[0], v2[1]))
        edge2 = list(bresenham(v1[0], v1[1], v3[0], v3[1]))
        edge3 = list(bresenham(v2[0], v2[1], v3[0], v3[1]))

        polygon_lines = [edge1, edge2, edge3]

        print("Equilateral Triangle raster edge list: ", polygon_lines)

        w = v2[0] + 1
        h = v3[1] + 1

        matrix = np.zeros((w, h))
        for edge in polygon_lines:
            for point in edge:
                matrix[point[0]][point[1]] = 255

        return matrix

    def raster_square(self, length):
        v1 = (0, 0)
        v2 = (length, 0)
        v3 = (length, length)
        v4 = (0, length)

        polygon_vertex_list = [v1, v2, v3, v4]

        print("Square vertex list: ", polygon_vertex_list)

        edge1 = list(bresenham(v1[0], v1[1], v2[0], v2[1]))
        edge2 = list(bresenham(v2[0], v2[1], v3[0], v3[1]))
        edge3 = list(bresenham(v3[0], v3[1], v4[0], v4[1]))
        edge4 = list(bresenham(v4[0], v4[1], v1[0], v1[1]))

        polygon_lines = [edge1, edge2, edge3, edge4]

        print("Square raster edge list: ", polygon_lines)

        w = length + 1
        h = length + 1

        matrix = np.zeros((w, h))
        for edge in polygon_lines:
            for point in edge:
                matrix[point[0]][point[1]] = 255

        return matrix

    def raster_hexagon(self, length):
        v1 = (length // 2, 0)
        v2 = (v1[0] + length, 0)
        v3 = (v2[0] + length // 2, v2[1] + int(length * math.sqrt(3)/2))
        v4 = (v3[0] - length // 2, v3[1] + int(length * math.sqrt(3)/2))
        v5 = (v4[0] - length, v4[1])
        v6 = (v5[0] - length // 2, v5[1] - int(length * math.sqrt(3)/2))

        polygon_vertex_list = [v1, v2, v3, v4, v5, v6]

        print("Hexagon vertex list: ", polygon_vertex_list)

        edge1 = list(bresenham(v1[0], v1[1], v2[0], v2[1]))
        edge2 = list(bresenham(v2[0], v2[1], v3[0], v3[1]))
        edge3 = list(bresenham(v3[0], v3[1], v4[0], v4[1]))
        edge4 = list(bresenham(v4[0], v4[1], v5[0], v5[1]))
        edge5 = list(bresenham(v5[0], v5[1], v6[0], v6[1]))
        edge6 = list(bresenham(v6[0], v6[1], v1[0], v1[1]))

        polygon_lines = [edge1, edge2, edge3, edge4, edge5, edge6]

        print("Hexagon raster edge list: ", polygon_lines)

        w = 2*length + 1
        h = int(math.sqrt(3)*length) + 1

        matrix = np.zeros((w, h))
        for edge in polygon_lines:
            for point in edge:
                matrix[point[0]][point[1]] = 255

        return matrix
