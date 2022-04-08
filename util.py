import matplotlib.pyplot as plt
from typing import List, Union, Optional, Tuple
import numpy as np
import os
import sys

line_offset = 0.2

def edgeUncertainty(x: int, x0: int) -> int:
    return x - x0


def arithmeticAvg(collection: List[Union[int, float]]) -> float:
    n = len(collection)
    return sum(collection) / n


def getFisherOf(n: int) -> float:
    fisher = {
        2: 1.837,
        3: 1.321,
        4: 1.197,
        5: 1.141,
        6: 1.110,
        7: 1.090,
        8: 1.077,
        9: 1.066,
        10: 1.059,
        11: 1.052,
        12: 1.047,
        13: 1.043,
        14: 1.040,
        15: 1.037,
        16: 1.034,
        17: 1.032,
        18: 1.030,
        19: 1.028,
        20: 1.027,
        25: 1.021,
        30: 1.018,
        35: 1.015,
        40: 1.013,
        45: 1.011,
        50: 1.010,
        100: 1.050,
        -1: 1
    }
    if 20 < n < 25:
        return fisher[20]
    if 25 < n < 30:
        return fisher[25]
    if 30 > n > 35:
        return fisher[30]
    if 35 > n > 40:
        return fisher[35]
    if 40 > n > 45:
        return fisher[40]
    if 45 > n > 50:
        return fisher[45]
    if 50 > n > 100:
        return fisher[50]
    if 100 > n > 1000:
        return fisher[100]
    if n >= 100:
        return fisher[-1]
    return fisher[n]


data = Union[int, float]

def average(values: List[data]):
    return sum(values) / len(values)

avg = average

def standard_deviation(wartosci: List[data]):
    N = len(wartosci)
    first_part = 1 / (N*(N-1))
    second_part = 0
    for i in wartosci:
        second_part += np.power(i - avg(wartosci), 2)

    return np.sqrt(first_part * second_part)

std_dev = standard_deviation

def linreg(argumenty: List[float], wartosci: List[float]):
    n = len(argumenty)
    if n != len(wartosci):
        raise Exception("Podano niewłaściwą ilość argumentów lub wartości")
    Sx = sum(argumenty)
    Sxx = sum([x * x for x in argumenty])
    Sy = sum(wartosci)
    Sxy = 0
    for i in range(len(argumenty)):
        Sxy += argumenty[i] * wartosci[i]
    a = (n * Sxy - Sx * Sy) / (n * Sxx - Sx * Sx)
    b = (Sxx * Sy - Sx * Sxy) / (n * Sxx - Sx * Sx)
    return a, b

def CtoK(T: float):
    return 273.15 + T


class MyPlotBase:
    def __init__(self, args: List[float], vals: List[float], erro: Optional[List[float]]):
        self.setArgs(args)
        self.setVals(vals)
        if erro:
            self.setErro(erro)
        else:
            self.setErro([])

    def setTitle(self, title: str):
        self._title = title

    def getTitle(self):
        return self._title

    def setArgs(self, args: List[float]):
        self._args = args

    def getArgs(self):
        return self._args

    def setVals(self, vals: List[float]):
        self._vals = vals

    def getVals(self):
        return self._vals

    def setErro(self, erro: List[float]):
        self._erro = erro

    def getErro(self):
        return self._erro



class MyPlot(MyPlotBase):

    def __init__(self, args: List[float], vals: List[float], erro: Optional[List[float]] = None):
        super().__init__(args, vals, erro)
        fig1, ax1 = plt.subplots()
        self.figure = fig1
        self.axes = ax1

    def plotLine(self, extended: Optional[bool] = False, **kwargs):
        args = self.getArgs()
        vals = self.getVals()
        self.axes.plot(args, vals, **kwargs)
        if(extended):
            plt.margins(-1 * line_offset)
        return self

    def addStyle(self, xLabel: str, yLabel:str):
        plt.minorticks_on()
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.grid()
        plt.title(self.getTitle())
        return self

    def boldAxes(self):
        self.axes.axhline(y=0, lw=3, color='k')
        self.axes.axvline(x=0, lw=3, color='k')

    def plotBars(self, args: Optional[List[float]] = None, vals: Optional[List[float]] = None, **kwargs):
        default_bars_style = ",r"
        if not args:
            args = self.getArgs()
        if not vals:
            vals = self.getVals()
        if not self.getErro():
            if not args or not vals:
                if not "xerr" in kwargs.keys() and not "yerr" in kwargs.keys():
                    raise Exception("No error data provided")
        else:
            kwargs["yerr"] = self.getErro()
        if not "fmt" in kwargs.keys():
            kwargs["fmt"] = default_bars_style
        if (len(args) != len(vals)):
            raise Exception("Invalid errorbar data given")

        self.axes.errorbar(args, vals, **kwargs)
        return self

    def setTitle(self, title: str):
        super().setTitle(title)
        plt.title(self.getTitle())


def load_data(path: str, manyValues: bool = True):
    data = {}
    realpath = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(realpath + "\\" + path, 'r') as f:
        filedata = [x.replace(',', '.').replace('\n', '').split('\t') for x in f.readlines()]

        arguments = [float(y) for y in [x[0] for x in filedata]]
        values = [[float(y) for y in x[1:]] for x in filedata]

        data["arguments"] = arguments
        data["values"] = values
        if not manyValues:
            data["values"] = [x[0] for x in data["values"]]
    return data

def statistical_uncertainty(values_matrix: List[List[float]]):
    return [std_dev(x) * getFisherOf(len(x)) for x in values_matrix]

def approx_linear(value, input: Tuple[float, float], output: Tuple[float, float]):
    input_range = input[0] - output[0]
    output_range = input[1] - output[1]
    slope = output_range / input_range
    return input[1] + slope * (value - input[0])