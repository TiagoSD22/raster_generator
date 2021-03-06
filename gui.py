import pathlib
import matplotlib as plt
import numpy as np
import pygubu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from line_raster import LineRaster
from polygon_raster import PolygonRaster

plt.use("TkAgg")

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "template.ui"

MAX_CACHE_SIZE = 50

class Application:
    def __init__(self, master=None):
        self.master = master

        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.resolution = 'AUTO'
        self.draw_data = None
        self.current_polygon = None
        self.mode = "LINE"
        self.line_raster = LineRaster()
        self.polygon_raster = PolygonRaster()
        self.cache = {}

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)

        builder.add_from_file(PROJECT_UI)

        self.main_window = builder.get_object("main_window", master)

        builder.connect_callbacks(self)

        self.draw_button = self.builder.get_object("draw_button", self.master)

        self.x1_entry = self.builder.get_object("x1_entry", self.master)
        self.y1_entry = self.builder.get_object("y1_entry", self.master)
        self.x2_entry = self.builder.get_object("x2_entry", self.master)
        self.y2_entry = self.builder.get_object("y2_entry", self.master)
        self.x1_label = self.builder.get_object("x1_label", self.master)
        self.y1_label = self.builder.get_object("y1_label", self.master)
        self.x2_label = self.builder.get_object("x2_label", self.master)
        self.y2_label = self.builder.get_object("y2_label", self.master)

        self.length_label = self.builder.get_object("length_label", self.master)
        self.length_entry = self.builder.get_object("length_entry", self.master)
        self.polygon_label = self.builder.get_object("polygon_label", self.master)
        self.polygon_combobox = self.builder.get_object("polygon_combobox", self.master)

        self.polygon_combobox["values"] = ["Equilateral Triangle", "Square", "Hexagon"]

        self.polygon_combobox.bind(
            "<<ComboboxSelected>>", self.polygon_combobox_handler
        )

        self.resolution_combobox = builder.get_object("resolution_combobox", master)

        self.resolution_combobox.current(0)

        self.resolution_combobox.bind("<<ComboboxSelected>>", self.resolution_combobox_handler)

        self.mode_combobox = builder.get_object("mode_combobox", master)

        self.mode_combobox.current(0)

        self.mode_combobox.bind("<<ComboboxSelected>>", self.mode_combobox_handler)

        self.fig = Figure(figsize=(10, 10))
        self.fig_subplot = self.fig.add_subplot(111)

        self.fig.set_facecolor("grey")

        self.fig_subplot.grid(which="minor", color="gray", linestyle="-", linewidth=2)

        self.canvas = self.builder.get_object("canvas", self.master)

        self.canvas = FigureCanvasTkAgg(self.fig, self.canvas)

        self.show_line_mode()

    def run(self):
        self.main_window.mainloop()

    def draw_raster(self):
        if self.mode == "LINE":
            self.draw_line_raster()
        else:
            self.draw_polygon_raster()

    def draw_line_raster(self):
        self.x1 = int(self.builder.get_object("x1_entry", self.master).get())
        self.y1 = int(self.builder.get_object("y1_entry", self.master).get())
        self.x2 = int(self.builder.get_object("x2_entry", self.master).get())
        self.y2 = int(self.builder.get_object("y2_entry", self.master).get())

        if self.resolution != 'AUTO':
            resolution = int(self.resolution.split('x')[0])

            old_width = abs(self.x2 - self.x1)
            old_height = abs(self.y2 - self.y1)

            old_width = 1 if old_width == 0 else old_width
            old_height = 1 if old_height == 0 else old_height

            self.x1 *= resolution // old_width
            self.x2 *= resolution // old_width
            self.y1 *= resolution // old_height
            self.y2 *= resolution // old_height

            self.fig_subplot.axis('off')

        self.line_raster.x1 = self.x1
        self.line_raster.y1 = self.y1
        self.line_raster.x2 = self.x2
        self.line_raster.y2 = self.y2

        raster = self.line_raster.draw_raster()

        if self.resolution == 'AUTO':
            self.fig_subplot.axis('on')
            self.fig_subplot.set_xticks(
                np.arange(-0.5, abs(self.line_raster.x2 - self.line_raster.x1), 1),
                minor=True,
            )
            self.fig_subplot.set_yticks(
                np.arange(-0.5, abs(self.line_raster.y2 - self.line_raster.y1), 1),
                minor=True,
            )

            xticks_values = [
                self.line_raster.repositioned_line[0][0],
                self.line_raster.repositioned_line[-1][0],
            ]
            xticks_values.sort()

            yticks_values = [
                self.line_raster.repositioned_line[0][1],
                self.line_raster.repositioned_line[-1][1],
            ]
            yticks_values.sort()

            xlabels_values = [self.line_raster.x1, self.line_raster.x2]
            xlabels_values.sort()

            ylabels_values = [self.line_raster.y1, self.line_raster.y2]
            ylabels_values.sort()

            self.fig_subplot.set_xticks(
                np.arange(xticks_values[0], xticks_values[1] + 1, 1)
            )
            self.fig_subplot.set_yticks(
                np.arange(yticks_values[0], yticks_values[1] + 1, 1)
            )
            self.fig_subplot.set_xticklabels(
                np.arange(xlabels_values[0], xlabels_values[1] + 1, 1)
            )
            self.fig_subplot.set_yticklabels(
                np.arange(ylabels_values[0], ylabels_values[1] + 1, 1)
            )

        self.draw_data = self.fig_subplot.imshow(
            raster.T, origin="lower", aspect="equal", interpolation=None, cmap="gray"
        )

        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

    def draw_polygon_raster(self):
        length = int(self.length_entry.get())
        resolution = self.resolution

        if self.resolution != 'AUTO':
            resolution = int(self.resolution.split('x')[0])
            length = resolution * length

            self.fig_subplot.axis('off')

        if self.current_polygon is not None:
            raster = self.get_from_cache(self.current_polygon, length, resolution)

            if raster is None:
                if self.current_polygon == "Equilateral Triangle":
                    raster = self.polygon_raster.raster_equilateral_triangle(length)
                    self.update_cache(self.current_polygon, length, resolution, raster)
                elif self.current_polygon == "Square":
                    raster = self.polygon_raster.raster_square(length)
                    self.update_cache(self.current_polygon, length, resolution, raster)
                    length *= 2
                else:
                    raster = self.polygon_raster.raster_hexagon(length)
                    self.update_cache(self.current_polygon, length, resolution, raster)
                    length *= 2
            else:
                if self.current_polygon != "Equilateral Triangle":
                    length *= 2

            if self.resolution == 'AUTO':
                self.fig_subplot.axis('on')

                self.fig_subplot.set_xticks(
                    np.arange(-0.5, length, 1),
                    minor=True,
                )
                self.fig_subplot.set_yticks(
                    np.arange(-0.5, length, 1),
                    minor=True,
                )

                self.fig_subplot.set_xticks(np.arange(0, length + 1, 1))
                self.fig_subplot.set_yticks(np.arange(0, length + 1, 1))
                self.fig_subplot.set_xticklabels(np.arange(0, length + 1, 1))
                self.fig_subplot.set_yticklabels(np.arange(0, length + 1, 1))

            self.draw_data = self.fig_subplot.imshow(
                raster.T,
                origin="lower",
                aspect="equal",
                interpolation=None,
                cmap="gray",
            )

            self.canvas.get_tk_widget().pack()
            self.canvas.draw()

    def resolution_combobox_handler(self, event):
        self.resolution = self.resolution_combobox.get()

    def mode_combobox_handler(self, event):
        self.mode = self.mode_combobox.get()

        if self.mode == "LINE":
            self.show_line_mode()
        else:
            self.show_polygon_mode()

    def polygon_combobox_handler(self, event):
        self.current_polygon = self.polygon_combobox.get()

    def show_line_mode(self):
        self.length_entry.grid_remove()
        self.length_label.grid_remove()
        self.polygon_combobox.grid_remove()
        self.polygon_label.grid_remove()

        self.resolution_combobox["values"] = ["AUTO", "30x30", "50x50", "100x100"]
        self.resolution_combobox.current(0)
        self.resolution = self.resolution_combobox.get()

        for e in [
            self.x1_entry,
            self.x1_label,
            self.x2_entry,
            self.x2_label,
            self.y1_entry,
            self.y1_label,
            self.y2_entry,
            self.y2_label,
        ]:
            e.grid()

    def show_polygon_mode(self):
        self.length_entry.grid()
        self.length_label.grid()
        self.polygon_combobox.grid()
        self.polygon_label.grid()

        self.resolution_combobox["values"] = ["AUTO", "10x10", "30x30", "50x50"]
        self.resolution_combobox.current(0)
        self.resolution = self.resolution_combobox.get()

        for e in [
            self.x1_entry,
            self.x1_label,
            self.x2_entry,
            self.x2_label,
            self.y1_entry,
            self.y1_label,
            self.y2_entry,
            self.y2_label,
        ]:
            e.grid_remove()

    def update_cache(self, polygon, length, resolution, raster):
        if len(self.cache) == MAX_CACHE_SIZE:
            self.cache.pop(next(iter(self.cache)))

        key = "{},{},{}".format(polygon, length, resolution)
        self.cache.update({key: raster})

    def get_from_cache(self, polygon, length, resolution):
        key = "{},{},{}".format(polygon, length, resolution)

        raster = None

        if key in self.cache.keys():
            raster = self.cache[key]

        return raster

