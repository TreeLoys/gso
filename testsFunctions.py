#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by treeloys at 06.04.22
"""

from abc import ABC, abstractmethod
import numpy as np

# Абстрактный класс для задания всех фитнесс функций
class TestFunction(ABC):
    @abstractmethod
    def calculateZ(self, x, y):
        pass

    @abstractmethod
    def getMinX(self):
        pass

    @abstractmethod
    def getMaxX(self):
        pass

    @abstractmethod
    def getMinY(self):
        pass

    @abstractmethod
    def getMaxY(self):
        pass


class Spherical(TestFunction):
    def calculateZ(self, x, y):
        return x ** 2.0 + y ** 2.0

    def getMinX(self):
        return -5

    def getMaxX(self):
        return 5

    def getMinY(self):
        return -5

    def getMaxY(self):
        return 5

    def getLevels(self):
        return 50

class Rastrigin(TestFunction):
    def calculateZ(self, X, Y):
        A = 10
        Z = 2 * A + X ** 2 - A * np.cos(2 * np.pi * X) + Y ** 2 - A * np.cos(2 * np.pi * Y)
        return Z

    def getMinX(self):
        return -5.52

    def getMaxX(self):
        return 5.12

    def getMinY(self):
        return -5.12

    def getMaxY(self):
        return 5.12

    def getLevels(self):
        return 100


class Ackley(TestFunction):
    def calculateZ(self, X, Y):
        Z = -20 * np.exp(-0.2 * np.sqrt(0.5 * (X**2 + Y**2))) - \
        np.exp(0.5 * (np.cos(2 * np.pi * X) + np.cos(2 * np.pi * Y))) + np.e + 20
        return Z
    
    def getMinX(self):
        return -5

    def getMaxX(self):
        return 5

    def getMinY(self):
        return -5

    def getMaxY(self):
        return 5

    def getLevels(self):
        return 18
    
    
class Beale(TestFunction):
    def calculateZ(self, X, Y):
        Z = np.power(1.5 - X + X * Y, 2) + np.power(2.25 - X + X * (Y ** 2), 2) \
        + np.power(2.625 - X + X * (Y ** 3), 2)
        return Z
    
    def getMinX(self):
        return -4.5

    def getMaxX(self):
        return 4.5

    def getMinY(self):
        return -4.5

    def getMaxY(self):
        return 4.5

    def getLevels(self):
        return 150000
    
    
class Booth(TestFunction):
    def calculateZ(self, X, Y):
        Z = np.power(X + 2*Y - 7, 2) + np.power(2 * X + Y - 5, 2)
        return Z
    
    def getMinX(self):
        return -10

    def getMaxX(self):
        return 10

    def getMinY(self):
        return -10

    def getMaxY(self):
        return 10

    def getLevels(self):
        return 2500
    
class Bukin(TestFunction):
    def calculateZ(self, X, Y):
        Z = 100 * np.sqrt(np.abs(Y - 0.01 * X**2)) + 0.01 * np.abs(X + 10)
        return Z
    
    def getMinX(self):
        return -15

    def getMaxX(self):
        return -5

    def getMinY(self):
        return -3

    def getMaxY(self):
        return 3

    def getLevels(self):
        return 200
    
    
class Three_humpCamel(TestFunction):
    def calculateZ(self, X, Y):
        Z = 2 * X**2 - 1.05 * X**4 + (1/6) * X**6 + X*Y + Y*2
        return Z
    
    def getMinX(self):
        return -5

    def getMaxX(self):
        return 5

    def getMinY(self):
        return -5

    def getMaxY(self):
        return 5

    def getLevels(self):
        return 2000
    
class Holder_table(TestFunction):
    def calculateZ(self, X, Y):
        Z = -np.abs(np.sin(X) * np.cos(Y) * np.exp(np.abs(1 - np.sqrt(X**2 + Y**2)/np.pi)))
        return Z
    
    def getMinX(self):
        return -10

    def getMaxX(self):
        return 10

    def getMinY(self):
        return -10

    def getMaxY(self):
        return 10

    def getLevels(self):
        return -20


class McCormick(TestFunction):
    def calculateZ(self, X, Y):
        Z = (np.sin(X+Y)+(X-Y)**2-1.5*X+2.5*Y+1)
        return Z

    def getMinX(self):
        return -1.5

    def getMaxX(self):
        return 4

    def getMinY(self):
        return -3

    def getMaxY(self):
        return 4

    def getLevels(self):
        return 40


class Shaffer(TestFunction):
    def calculateZ(self, X, Y):
        def f(x, y):  # Defines the function
            num = (np.sin((x ** 2 + y ** 2) ** 2) ** 2) - 0.5
            den = (1 + 0.001 * (x ** 2 + y ** 2)) ** 2
            return 0.5 + num / den

        Z = f(X, Y)
        return Z

    def getMinX(self):
        return -10

    def getMaxX(self):
        return 10

    def getMinY(self):
        return -10

    def getMaxY(self):
        return 10

    def getLevels(self):
        return 1
    
    
    
    
    
    
    
    
