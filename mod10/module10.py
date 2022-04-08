from typing import Tuple
from util import *
from lat import LatexParser
import math

ROOT = math.sqrt(3)


def getBUncertainty(v, clas, precision):
    return (abs(v) * clas + 1 * precision) / ROOT


def main():
    d = load_data("data10.txt", manyValues=False)
    arguments, values = d.values()

    arguments1, arguments2 = arguments[0:6], arguments[6:]
    values1, values2 = values[0:6], values[6:]

    uI = [getBUncertainty(x, 0.02, 0.01) for x in arguments]
    uT = [getBUncertainty(x, 0.005, 0.1) for x in values]
    uI1, uI2 = uI[:6], uI[6:]
    uT1, uT2 = uT[:6], uT[6:]

    fig1, ax1 = plt.subplots()


    ax1.errorbar(arguments1, values1, xerr=uI1, yerr=uT1, fmt=",b", label="brak polaryzacji", capsize=2)
    ax1.errorbar(arguments2, values2, xerr=uI2, yerr=uT2, fmt=",r", label="polaryzacja", capsize=2)
    plt.legend(loc="upper left")
    plt.minorticks_on()
    plt.xlabel(r"I - natężenie prądu [A]")
    plt.ylabel(r"$\Delta$T - różnica temperatury [K]")
    plt.grid()
    plt.title("wykres różnicy temperatury od natężenia prądu")

    offset = 0.5

    a1, b1 = linreg(arguments1, values1)
    x = np.linspace(min(arguments1)-offset, max(arguments1)+offset)
    y = x * a1 + b1

    a2, b2 = linreg(arguments2, values2)
    x2 = np.linspace(min(arguments2)-offset, max(arguments2)+offset)
    y2 = x2 * a2 + b2

    fig2, ax2 = plt.subplots()
    ax2.plot(x, y, "-b")
    ax2.plot(x2, y2, "-r")
    ax2.errorbar(arguments1, values1, xerr=uI1, yerr=uT1, fmt=",b", label="brak polaryzacji", capsize=2)
    ax2.errorbar(arguments2, values2, xerr=uI2, yerr=uT2, fmt=",r", label="polaryzacja", capsize=2)
    plt.legend(loc="upper left")

    plt.minorticks_on()
    plt.xlabel(r"I - natężenie prądu [A]")
    plt.ylabel(r"$\Delta$T - różnica temperatury [K]")
    plt.grid()
    plt.title("wykres regresji liniowej różnicy temperatury od natężenia prądu")
    plt.show()

    print(a1, b1)
    print(a2, b2)
    a, b = linreg(arguments, values)
    x = np.linspace(min(arguments)-offset, max(arguments)+offset)
    y = x * a + b
    print(a, b)
"""
    Pojedyńcza
  offset = 1

    a, b = linreg(arguments, values)
    x = np.linspace(min(arguments)-offset, max(arguments)+offset)
    y = x * a + b

    a2, b2 = linreg(arguments2, values2)
    x2 = np.linspace(min(arguments2)-offset, max(arguments2)+offset)
    y2 = x2 * a2 + b2

    fig2, ax2 = plt.subplots()
    ax2.plot(x, y, "-g")

    ax2.errorbar(arguments1, values1, xerr=uI1, yerr=uT1, fmt=",b", label="brak polaryzacji", capsize=2)
    ax2.errorbar(arguments2, values2, xerr=uI2, yerr=uT2, fmt=",r", label="polaryzacja", capsize=2)
    plt.legend(loc="upper left")

    plt.minorticks_on()
    plt.xlabel(r"I - natężenie prądu [A]")
    plt.ylabel(r"$\Delta$T - różnica temperatury [K]")
    plt.grid()
    plt.title("wykres regresji liniowej różnicy temperatury od natężenia prądu")
"""







if __name__ == "__main__":
    main()