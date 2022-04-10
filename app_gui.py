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


class Application:
    def __init__(self, master=None):
        self.master = master

        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.resolution = None
        self.draw_data = None
        self.current_polygon = None
        self.mode = 'LINE'
        self.line_raster = LineRaster()
        self.polygon_raster = PolygonRaster()

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)

        builder.add_from_file(PROJECT_UI)

        self.main_window = builder.get_object("main_window", master)

        builder.connect_callbacks(self)

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

        self.polygon_combobox.bind('<<ComboboxSelected>>', self.polygon_combobox_handler)

        self.show_line_mode()

        self.resolution_combobox = builder.get_object("resolution_combobox", master)

        self.resolution_combobox.current(0)

        self.mode_combobox = builder.get_object("mode_combobox", master)

        self.mode_combobox.current(0)

        self.mode_combobox.bind('<<ComboboxSelected>>', self.mode_combobox_handler)

        self.fig = Figure(figsize=(10, 10))
        self.fig_subplot = self.fig.add_subplot(111)

        self.fig_subplot.grid(which="minor", color="r", linestyle="-", linewidth=2)

        self.canvas = self.builder.get_object("canvas", self.master)

        self.canvas = FigureCanvasTkAgg(self.fig, self.canvas)

    def run(self):
        self.main_window.mainloop()

    def draw_raster(self):
        if self.mode == 'LINE':
            self.draw_line_raster()
        else:
            self.draw_polygon_raster()

    def draw_line_raster(self):
        self.x1 = self.builder.get_object("x1_entry", self.master).get()
        self.y1 = self.builder.get_object("y1_entry", self.master).get()
        self.x2 = self.builder.get_object("x2_entry", self.master).get()
        self.y2 = self.builder.get_object("y2_entry", self.master).get()

        self.line_raster.x1 = int(self.x1)
        self.line_raster.y1 = int(self.y1)
        self.line_raster.x2 = int(self.x2)
        self.line_raster.y2 = int(self.y2)

        raster = self.line_raster.draw_raster()

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

        if self.current_polygon is not None:
            if self.current_polygon == 'Equilateral Triangle':
                raster = self.polygon_raster.raster_equilateral_triangle(length)

            elif self.current_polygon == 'Square':
                pass

            else:
                pass

            self.draw_data = self.fig_subplot.imshow(
                raster.T, origin="lower", aspect="equal", interpolation=None, cmap="gray"
            )

            self.canvas.get_tk_widget().pack()
            self.canvas.draw()

    def mode_combobox_handler(self, event):
        self.mode = self.mode_combobox.get()

        if self.mode == 'LINE':
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

        for e in [self.x1_entry, self.x1_label, self.x2_entry, self.x2_label, self.y1_entry, self.y1_label, self.y2_entry, self.y2_label]:
            e.grid()

    def show_polygon_mode(self):
        self.length_entry.grid()
        self.length_label.grid()
        self.polygon_combobox.grid()
        self.polygon_label.grid()

        for e in [self.x1_entry, self.x1_label, self.x2_entry, self.x2_label, self.y1_entry, self.y1_label,
                  self.y2_entry, self.y2_label]:
            e.grid_remove()