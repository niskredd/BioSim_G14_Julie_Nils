# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''


import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


class Visual_Plot:

    def __init__(self):
        style.use('fivethirtyeight')

        fig = plt.figure()
        self.ax1 = fig.add_subplot(1, 1, 1)
        open('plotdata.csv', 'w')

    def animate(self):
        graph_data = open('plotdata.csv', 'a').read()
        lines = graph_data.split('\n')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(float(x))
                ys.append(float(y))
        self.ax1.clear()
        self.ax1.plot(xs, ys)
