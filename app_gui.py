import pathlib

import matplotlib as plt
import numpy as np
import pygubu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from line_raster import LineRaster

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
        self.mode = 'LINE'
        self.line_raster = LineRaster()

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)

        builder.add_from_file(PROJECT_UI)

        self.main_window = builder.get_object("main_window", master)

        builder.connect_callbacks(self)

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
            # TODO draw polygon raster
            pass

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

    def mode_combobox_handler(self, event):
        self.mode = self.mode_combobox.get()
