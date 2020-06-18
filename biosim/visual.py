# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Martin, Nils Skreddernes'
__email__ = ''
import numpy as np
import matplotlib.pyplot as plt


class Visualization:
    """This is the visualization class"""

    def __init__(self):
        self.steps = 0
        self.herb_data = []
        self.carn_data = []

    def set_plots_for_first_time(self, rgb_map=None, herb_htmp_data= None, carn_htmp_data=None):
        """
        Sets up the visualization for the first time
        :param rgb_map: list of rgb values
        :param herb_htmp_data: herbivore data
        :param carn_htmp_data: carnivore data
        :return: none
        """
        self.fig = plt.figure(figsize=(15, 10))
        plt.axis('off')
        self.step_len = 0

        self.fit_plot = self.fig.add_subplot(6, 3, 16)
        self.fit_plot.title.set_text('Fitness Histogram')
        self.fit_axis = None
        self.age_plot = self.fig.add_subplot(6, 3, 17)
        self.age_plot.title.set_text('Age Histogram')
        self.weight_plot = self.fig.add_subplot(6, 3, 18)
        self.weight_plot.title.set_text('Weight Histogram')

        """
            Heat maps setup                 """
        self.herb_heatmap_axis = self.fig.add_axes([0.1, 0.28, 0.35, 0.3])  # llx, lly, w, h
        self.herb_axis = None
        self.herb_heatmap_axis.title.set_text('Herb Heatmap')
        self.herb_heatmap_axis.set_yticklabels([])
        self.herb_heatmap_axis.set_xticklabels([])

        self.carn_heatmap_axis = self.fig.add_axes([0.55, 0.28, 0.35, 0.3])  # llx, lly, w, h
        self.carn_axis = None
        self.carn_heatmap_axis.title.set_text('Carn Heatmap')
        self.carn_heatmap_axis.set_yticklabels([])
        self.carn_heatmap_axis.set_xticklabels([])

        """
            Island map set up only called once in the beginning """
        self.island_axis =  self.fig.add_axes([0.1, 0.65, 0.35, 0.3])  # llx, lly, w, h
        self.island_axis.title.set_text('Island Map')
        self.island_axis.set_yticklabels([])
        self.island_axis.set_xticklabels([])
        self.island_axis.imshow(rgb_map)

        """
            Line plot           """
        self.line_axis =  self.fig.add_axes([0.55, 0.65, 0.35, 0.3])  # llx, lly, w, h

        """
            Age count text          """
        self.year_txt = self.fig.add_axes([0.45, 0.95, 0.02, 0.02])
        self.year_txt.axis('off')
        self.changing_text = self.year_txt.text(0.2, 0.5, "Year: "+str(0)
                                                , fontdict= { 'weight': 'bold', 'size': 16 })
        plt.pause(1e-6)

    def update_plot(self, anim_distribution_dict=None, total_anim_dict=None):
        self.steps += self.step_len
        """
            Changing the Year in the text       """
        self.changing_text.set_text( "Year: "+str(self.steps))

        """
            Updating the herbivore heatmap          """
        if self.herb_axis is None:
            self.herb_axis = self.herb_heatmap_axis.imshow(anim_distribution_dict['Herbivore'],
                                                           interpolation='nearest',
                                                           cmap="Greens", vmin=0, vmax=50)
            self.herb_heatmap_axis.figure.colorbar(self.herb_axis, ax=self.herb_heatmap_axis,
                                                   orientation='horizontal',
                                                   fraction=0.07, pad=0.04)
        else:
             self.herb_axis.set_data(anim_distribution_dict['Herbivore'])

        """
            Updating the carnivore heatmap          """

        if self.carn_axis is None:
            self.carn_axis = self.carn_heatmap_axis.imshow(anim_distribution_dict['Carnivore'],
                                                           interpolation='nearest',
                                                           cmap="OrRd", vmin=0, vmax=50)
            self.carn_heatmap_axis.figure.colorbar(self.carn_axis, ax=self.carn_heatmap_axis,
                                                   orientation='horizontal',
                                                   fraction=0.07, pad=0.04)
        else:
             self.carn_axis.set_data(anim_distribution_dict['Carnivore'])


        """
            Updating the line graphs            """
        self.herb_data.append(total_anim_dict['Herbivore'])
        self.carn_data.append(total_anim_dict['Carnivore'])
        length = len(self.carn_data)
        x = list(np.arange(length))
        # self.line_ax.clear()
        self.line_axis.set_ylim(0, max(self.herb_data) + 10)

        self.line_axis.title.set_text('Herb and Carn Count in map')
        self.line_axis.set_xlabel('Years')
        self.line_axis.set_ylabel('Number of Species')

        self.line_axis.plot(x, self.herb_data, '-', color='g', linewidth=0.5)
        self.line_axis.plot(x, self.carn_data, '-', color ='r', linewidth=0.5)

        plt.pause(1e-6)

    def set_step_ln(self, s_len):
            self.step_len = s_len

    def update_histogram(self, fit_list=None, age_list=None, weight_list=None):
        """
        updates all the histograms
        :param fit_list: list of dictionary
        :param age_list: list of dictionary
        :param weight_list: list of dictionary
        :return: none
        """
        self.fit_plot.clear()
        self.fit_plot.title.set_text('Fitness Histogram')
        self.fit_plot.hist(fit_list['Herbivore'], bins=10, histtype='step')
        self.fit_plot.hist(fit_list['Carnivore'], bins=10, histtype='step')

        self.age_plot.clear()
        self.age_plot.title.set_text('Age Histogram')
        self.age_plot.hist(age_list['Herbivore'], bins=10, histtype='step')
        self.age_plot.hist(age_list['Carnivore'], bins=10, histtype='step')

        self.weight_plot.clear()
        self.weight_plot.title.set_text('Weight Histogram')
        self.weight_plot.hist(weight_list['Herbivore'], bins=10, histtype='step')
        self.weight_plot.hist(weight_list['Carnivore'], bins=10, histtype='step')
