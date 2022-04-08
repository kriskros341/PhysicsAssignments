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
    eta_from_avg_time = [eq(approx_linear(arguments[i], (20, 878.8), (50, 857.5)), average_values[i]) for i in range(len(arguments))]
    eta_uncertainty = [eq(approx_linear(arguments[i], (20, 878.8), (50, 857.5)), czasomierz_Ub) for i in range(len(arguments))]
    w2 = MyPlot(arguments, eta_from_avg_time)
    w2.setTitle("Wykres wsp. lepkości od temperatury")
    w2.addStyle(r'T - temperatura [${}^{\circ}C$]', r'$\eta$ - współczynnik lepkości [$\frac{kg}{ms}$]')
    print(eta_uncertainty)
    w2.plotBars(xerr=czasomierz_Ub, yerr=eta_uncertainty, capsize=2)

    newA = [1/CtoK(x) for x in arguments]
    newB = [math.log(x) for x in eta_from_avg_time]

    w3 = MyPlot(newA, newB)
    w3.setTitle("Wykres logarytmu naturalnego wsp. lepkości od odwrotności temperatury")
    w3.addStyle(r'$\frac{1}{T}$ - temperatura [$K$]', r'$\ln{\eta}$ - logarytm naturalny współczynnika lepkości [$\frac{kg}{ms}$]')
    w3.plotBars([1/x for x in arguments], [math.log(x) for x in eta_from_avg_time], yerr=eta_uncertainty, capsize=2)


    a, b = linreg(arguments, eta_from_avg_time)
    x = np.linspace(min(arguments) - 10, max(arguments) + 10)
    y = x * a + b

    #w4 = MyPlot(x, y)
    #w4.setTitle("Wykres regresji liniowej")
    #w4.addStyle(r"temperatura", r"wsp. lepkosci")
    #w4.plotLine()
    #w4.plotBars(arguments, eta_uncertainty,  ecolor='r', capsize=2)

    w4 = MyPlot(x, y, eta_uncertainty)

    w4.setTitle(r'Wykres regresji liniowej')
    # plt.margins(-1 * line_offset)
    w4.addStyle(r'T - temperatura [${}^{\circ}C$]', r'$\eta$ - współczynnik lepkości [$\frac{kg}{ms}$]')
    w4.plotLine(extended=True).plotBars(arguments, eta_from_avg_time, ecolor='r', capsize=2)

    a, b = linreg(newA, newB)

    x = np.linspace(min(arguments) - 10, max(arguments) + 10)
    y = x * a + b

    w5 = MyPlot(x, y)
    w5.setTitle("Nie mam pojęcia")
    w5.addStyle(r'Wpisać', r'Co tu')
    w5.plotLine()



    e = [eta_from_avg_time[i] - a * arguments[i] - b for i in range(len(arguments))]
    See = sum(x*x for x in e)
    #print(See)
    n = len(arguments)
    common = n/(n-2) * See/(n*sum(x*x for x in arguments) - sum(arguments))
    Ua = math.sqrt(common)
    Ub = math.sqrt(sum(x*x for x in arguments) * common)
    #print(Ua, Ub)

    l = LatexParser("../")
    #print(l.gen_tex_boilerplate(extended=True, uncertain=False, rounding=4, X=arguments, Y=eta_from_avg_time, signX=r"T", signY=r"\eta"))
    #plt.show()
    #print(a, b)
    print(newA, newB)
    print(a, b)
    
    #print(l.gen_tex_boilerplate(extended=True, uncertain=False, rounding=4, X=[x for x in newA], Y=[x for x in newB], signX=r"T", signY=r"\eta"))



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