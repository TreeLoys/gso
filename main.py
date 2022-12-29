#!/usr/bin/env python
# Created by Valera at 17.12.2022

import numpy as np
from numpy import arange
from numpy import meshgrid
from matplotlib import pyplot

import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import matplotlib.cm


from glowworm import starting_points, get_score, influence_matrix, next_turn


import copy

# Эволюция, он же менеджер эпох, служит для сбора всей доступной информации по работе алгоритма GSO
class Evolution():
    def __init__(self, settings):
        self.settings = settings
        self.iteration = settings.iteration
        self.population = settings.populationSize # Объект популяции
        self.bestStep = []
        self.bestPatchesByStep = []

    # Запускает алгоритм GSO
    def run(self):
        # Расчет позиции светлячков
        pop = starting_points(self.settings)
        # Считаем каждую эпоху и сохраняем координаты всего что можно
        for each in range(self.iteration):
            # Считаем позиции светлячков и фитнесс функций
            score = get_score(pop, self.settings)

            # Круги светимости светлячков
            patches = []
            for i in range(0, self.population):
                patches.append(mpatches.Circle((pop[i][0], pop[i][1]), score[i], ec="none"))

            self.bestStep.append({"x": pop[:, 0], "y": pop[:, 1]})
            self.bestPatchesByStep.append(patches)
            # Расчет матрицы влияния и новой эпохи
            im = influence_matrix(pop, score, self.population)
            pop = copy.deepcopy(next_turn(pop, score, im, self.settings))

    # Отрисовка фигуры начального вида графика
    def drawInitArea(self):
        # Построения графика
        xaxis = arange(self.settings.testFunction.getMinX(),
                       self.settings.testFunction.getMaxX(), 0.1)
        yaxis = arange(self.settings.testFunction.getMinY(),
                       self.settings.testFunction.getMaxY(), 0.1)
        x, y = meshgrid(xaxis, yaxis)
        results = self.settings.testFunction.calculateZ(x, y)
        figure = pyplot.figure(figsize=(8, 7))
        axis = figure.gca(projection='3d')

        axis.plot_surface(x, y, results, cmap='jet')
        # axis.plot_wireframe(x, y, results)
        # pyplot.show()
        return figure

    # Отображение позиции светлячков на заданной эпохе
    def drawGlowwormsByStep(self, step):
        # Общая часть
        fig = pyplot.figure(figsize=(8, 7))
        left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
        ax = fig.add_axes([left, bottom, width, height])
        ax.set_title("2D Пространство")

        xaxis = arange(self.settings.testFunction.getMinX(),
                       self.settings.testFunction.getMaxX(), 0.1)
        yaxis = arange(self.settings.testFunction.getMinY(),
                       self.settings.testFunction.getMaxY(), 0.1)
        x, y = meshgrid(xaxis, yaxis)
        results = self.settings.testFunction.calculateZ(x, y)
        if self.settings.testFunction.getLevels() > 0:
            cp = pyplot.contourf(x, y, results, levels=np.linspace(0,
                                                                   self.settings.testFunction.getLevels(),
                                                                   50))
        else:
            cp = pyplot.contourf(x, y, results, levels=np.linspace(self.settings.testFunction.getLevels(),
                                                                   0,
                                                                   50))
        pyplot.colorbar(cp)

        # Отображение алгоритма
        if step < len(self.bestStep):
            pyplot.scatter(self.bestStep[step]["x"], self.bestStep[step]["y"],
                           s=1, c="red"
                           )


            # Градиентные кружки
            colors = np.linspace(0, 1, len(self.bestPatchesByStep[0]))
            collection = PatchCollection(self.bestPatchesByStep[step], cmap=matplotlib.cm.get_cmap("Greys"), alpha=0.05)
            collection.set_array(np.array(colors))
            ax.add_collection(collection)
        return fig