from typing import Tuple
from util import *

from lat import LatexParser
import math

"""
pierwiastki_wysokosci = [4, 4]
srednie_t = [4, 4]

print(gen_tex_table(
    headers=[r"test", "test"],
    data=[["{:.3f}".format(x) for x in pierwiastki_wysokosci],
          ["{:.3f}".format(x) for x in srednie_t]]))
"""

def eq(Pc, t):
    K = 1.2018 * 10**-6
    Pk = 8150
    print(Pk, Pc, K, t)
    return K * (Pk - Pc) * t


def main():
    arguments, values = load_data("data8.txt").values()
    average_values = [avg(x) for x in values]
    Ua = statistical_uncertainty(values)
    print("avg czas:", average_values)
    print("Ua", Ua)
    a = 0.005  # TYMCZASOWE
    b = 0.001  # TYMCZASOWE
    czasomierz_Ub = (0.2 + 0.01)
    termometr_Ub = 0.5
    niepewnosc_calkowita = [np.sqrt(Ua[i]**2 + termometr_Ub**2) for i in range(len(arguments))]
    print(niepewnosc_calkowita)
    """
    w1 = MyPlot(arguments, average_values, niepewnosc_calkowita)
    w1.setTitle("wykres1")
    w1.addStyle(r"wsp. lepkosci", r"temperatura")
    w1.plotBars(capsize=2)
    """
    density_of_oil = [approx_linear(x, (20, 878.8), (50, 857.5)) for x in arguments]
    #l = LatexParser("..\\")
    #print(l.gen_tex_table(["doil"], density_of_oil))
    micro_from_avg_time = [eq(approx_linear(arguments[i], (20, 878.8), (50, 857.5)), average_values[i]) for i in range(len(arguments))]
    micro_uncertainty = [eq(approx_linear(arguments[i], (20, 878.8), (50, 857.5)), czasomierz_Ub) for i in range(len(arguments))]
    w2 = MyPlot(arguments, micro_from_avg_time)
    w2.setTitle("Wykres wsp. lepkości od temperatury")
    w2.addStyle(r"temperatura", r"wsp. lepkosci")
    print(micro_uncertainty)
    w2.plotBars(xerr=czasomierz_Ub, yerr=micro_uncertainty, capsize=2)

    w3 = MyPlot([1/x for x in arguments], [math.log(x) for x in micro_from_avg_time])
    w3.setTitle("Wykres logarytmu naturalnego wsp. lepkości od odwrotności temperatury")

    w3.addStyle(r"1/temperatura", r"ln(wsp. lepkosci)")
    w3.plotLine()

    a, b = linreg(arguments, micro_from_avg_time)
    x = np.linspace(min(arguments) - line_offset, max(micro_from_avg_time) + line_offset)
    y = x * a + b

    w4 = MyPlot(x, y)
    w4.setTitle("Wykres regresji liniowej")
    w4.addStyle(r"temperatura", r"wsp. lepkosci")
    w4.plotLine(extended=True)


    plt.show()
"""
    w3 = MyPlot([1/x for x in arguments], [x for x in density_of_oil])
    w3.setTitle("w2")
    w3.addStyle(r"temperatura", r"wsp. lepkosci")
    w3.plotBars(xerr=niepewnosc_calkowita)
"""

    #for i in density_of_oil:
    #    print("{:.3f}".format(i))






if __name__ == '__main__':
    main()