from typing import Tuple
from util import *
from lat import LatexParser
"""
pierwiastki_wysokosci = [4, 4]
srednie_t = [4, 4]

print(gen_tex_table(
    headers=[r"test", "test"],
    data=[["{:.3f}".format(x) for x in pierwiastki_wysokosci],
          ["{:.3f}".format(x) for x in srednie_t]]))
"""

def eq(Pc, dt):
    K = 1.2018 * 10**-6
    Pk = 8150
    return K * (Pk - Pc) * dt


def main():
    arguments, values = load_data("data8.txt").values()
    average_values = [avg(x) for x in values]
    Ua = statistical_uncertainty(values)
    print("avg czas:", average_values)
    print("Ua", Ua)
    a = 0.005  # TYMCZASOWE
    b = 0.001  # TYMCZASOWE
    niepewnosc_typu_b = [(x * a + 5 * b) / np.sqrt(3) for x in average_values]
    print(niepewnosc_typu_b)
    niepewnosc_calkowita = [np.sqrt(Ua[i]**2 + niepewnosc_typu_b[i]**2) for i in range(len(arguments))]
    print(niepewnosc_calkowita)
    w1 = MyPlot(arguments, average_values, niepewnosc_calkowita)
    w1.setTitle("wykres1")
    w1.addStyle(r"wsp. lepkosci", r"temperatura")
    w1.plotBars(capsize=2)

    density_of_oil = [approx_linear(x, (20, 878.8), (50, 857.5)) for x in arguments]
    l = LatexParser("..\\")
    print(l.gen_tex_table(["doil"], density_of_oil))

    w2 = MyPlot(arguments, density_of_oil, niepewnosc_calkowita)
    w2.setTitle("w2")
    w2.plotBars()

    for i in density_of_oil:
        print("{:.3f}".format(i))

    plt.show()




if __name__ == '__main__':
    main()