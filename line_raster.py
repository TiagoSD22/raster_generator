from typing import List, Tuple
import numpy as np
from bresenham import bresenham


class LineRaster:
    def __init__(self, x1=None, y1=None, x2=None, y2=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.line_points = []
        self.repositioned_line = []

    def draw_raster(self):
        self.line_points = list(bresenham(self.x1, self.y1, self.x2, self.y2))

        print("Raster line points: ", self.line_points)

        self.repositioned_line = self.__reposition_line()

        print("Raster repositioned line points: ", self.repositioned_line)

        self.line_points = self.repositioned_line

        data = self.__draw_raster_line_image()

        return data

    def __reposition_line(self) -> List[Tuple[float, float]]:
        minimum_x = min(list(zip(*self.line_points))[0])  # obtém o menor valor x entre todos os pontos
        minimum_y = min(list(zip(*self.line_points))[1])  # obtém o menor valor y entre todos os pontos

        repositioned_line: List[Tuple[float, float]] = list(
            map(
                # cada ponto tem suas coordenadas x,y decrementadas, respectivamente,
                # do x e y mínimos encontrados anteriormente
                lambda point: (point[0] - minimum_x, point[1] - minimum_y),
                self.line_points,
            )
        )

        return repositioned_line

    def __scale_line(self, new_w, new_h):
        w = abs(self.line_points[-1][0] - self.line_points[0][0]) + 1
        h = abs(self.line_points[-1][1] - self.line_points[0][1]) + 1

        new_y = int(2 * new_h / h * self.line_points[-1][1])
        new_x = int(2 * new_w / w * self.line_points[-1][0])

        return list(
            bresenham(self.line_points[0][0], self.line_points[0][1], new_x, new_y)
        )

    def __draw_raster_line_image(self):
        # self.line_points contém a lista de pontos retornada pelo algoritmo de Bresenham
        w = abs(self.line_points[-1][0] - self.line_points[0][0]) + 1
        h = abs(self.line_points[-1][1] - self.line_points[0][1]) + 1

        if h == 1:  # caso excepcional para semi-retas paralelas ao eixo x
            h += 1
        if w == 1:  # caso excepcional para semi-retas paralelas ao eixo y
            w += 1

        matrix = np.zeros((w, h))  # matriz inicializada com todos as células = 0 (pixels pretos)
        for point in self.line_points:
            # coordenada presente na lista de Bresenham,
            # logo a célula será interceptada pela semi-reta e deve ter seu valor = 1 (pixel branco)
            matrix[point[0]][point[1]] = 255

        print(np.rot90(matrix))
        return matrix
