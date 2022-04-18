import math
import numpy as np
from bresenham import bresenham
import copy
from scipy.ndimage.interpolation import rotate


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

        return self.__create_raster(polygon_lines, w, h)

    def raster_square(self, length):
        v1 = (length//2, length//2)
        v2 = (v1[0] + length, v1[1])
        v3 = (v2[0], v2[1] + length)
        v4 = (v3[0] - length, v3[1])

        polygon_vertex_list = [v1, v2, v3, v4]

        print("Square vertex list: ", polygon_vertex_list)

        edge1 = list(bresenham(v1[0], v1[1], v2[0], v2[1]))
        edge2 = list(bresenham(v2[0], v2[1], v3[0], v3[1]))
        edge3 = list(bresenham(v3[0], v3[1], v4[0], v4[1]))
        edge4 = list(bresenham(v4[0], v4[1], v1[0], v1[1]))

        polygon_lines = [edge1, edge2, edge3, edge4]

        print("Square raster edge list: ", polygon_lines)

        w = v2[0] - v1[0] + length + 1
        h = v4[1] - v1[1] + length + 1

        return self.__create_raster(polygon_lines, w, h)

    def raster_hexagon(self, length):
        v1 = (length // 2, 0)
        v2 = (v1[0] + length, 0)
        v3 = (v2[0] + length // 2, v2[1] + int(length * math.sqrt(3) / 2))
        v4 = (v3[0] - length // 2, v3[1] + int(length * math.sqrt(3) / 2))
        v5 = (v4[0] - length, v4[1])
        v6 = (v5[0] - length // 2, v5[1] - int(length * math.sqrt(3) / 2))

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

        w = 2 * length + 1
        h = int(math.sqrt(3) * length) + 1

        return self.__create_raster(polygon_lines, w, h)

    def __create_raster(self, edge_list, w, h):
        matrix = np.zeros((w, h))
        for edge in edge_list:
            for point in edge:
                matrix[point[0]][point[1]] = 255

        return self.__fill_polygon(matrix)

    def __is_internal_vertex(self, x, y, raster):
        (
            left_side_intersections_counter,
            right_side_intersections_counter,
        ) = self.__count_scam_line_interactions_from_point(x, y, raster)

        is_right_intersections_odd = (
            True if right_side_intersections_counter % 2 == 1 else False
        )
        is_left_intersections_odd = (
            True if left_side_intersections_counter % 2 == 1 else False
        )

        return is_left_intersections_odd and is_right_intersections_odd

    def __count_scam_line_interactions_from_point(self, x, y, raster):
        right_side_intersections_counter = 0
        left_side_intersections_counter = 0

        # count intersections from point to right border
        for column in range(y, len(raster[x])):
            if raster[x][column] == 255:
                right_side_intersections_counter += 1

        # count intersections from point to left border
        for column in range(y, -1, -1):
            if raster[x][column] == 255:
                left_side_intersections_counter += 1

        return left_side_intersections_counter, right_side_intersections_counter

    def __fill_polygon(self, raster):
        raster = np.rot90(raster)
        dc = copy.deepcopy(raster)

        for row in range(len(raster)):
            for column in range(len(raster[row])):
                if self.__is_internal_vertex(row, column, raster):
                    dc[row][column] = 255

        dc = rotate(dc, angle=-90)

        return dc
