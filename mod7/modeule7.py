from typing import List, Union, Optional
import matplotlib.pyplot as plt
import numpy as np
from util import *
from lat import LatexParser

line_offset = 0.2

def main():
    with open("data7.txt") as f:
        filedata = [x for x in f.readlines()]
        wysokosci = [float(y.replace(',', '.')) for y in [x.split('\t')[0] for x in filedata]]

        matryca_stringow = [x[4:-1].split('\t') for x in filedata]

        matryca_czasow = []
        for row in matryca_stringow:
            current_row = []
            for value in row:
                current_row.append(float(value.replace(',', '.')))
            matryca_czasow.append(current_row)

        pierwiastki_wysokosci = [np.sqrt(x) for x in wysokosci] # 1
        srednie_t = [avg(x) for x in matryca_czasow] # 2
        niepewnosci_statystyczne_serii = statistical_uncertainty(matryca_czasow)
        niepewnosci_calkowite = []
        for i in range(len(srednie_t)):
            print("wartosci pomiarów dla wysokosci", wysokosci[i], ":", matryca_czasow[i])
            print("pierwiastek wysokosci:", pierwiastki_wysokosci[i])
            print("srednia pomiarów:", srednie_t[i])
            print("niepewnosci_statystyczne_serii:", niepewnosci_statystyczne_serii[i])
            a = 0.005  # specyfikacja urządzenia pomiarowego
            b = 0.001  # specyfikacja urządzenia pomiarowego
            niepewnosc_typu_b = (srednie_t[i] * a + 5*b)/np.sqrt(3)
            print("Niepewność standardowa typu b dla średniej to", niepewnosc_typu_b)
            niepewnosc_calkowita = np.sqrt(niepewnosci_statystyczne_serii[i]**2 + niepewnosc_typu_b**2)
            print("niepewność całkowita:", niepewnosc_calkowita)
            niepewnosci_calkowite.append(niepewnosc_calkowita)

            print("-----------------------------------------")

        w1 = MyPlot(wysokosci, srednie_t, niepewnosci_calkowite)
        w1.setTitle("Wykres zależności średniego czasu spadania od H")
        w1.addStyle(r'$H$ - wysokości [m]', r'$t_{śr}$ - średni czas spadania [s]')
        w1.plotBars(ecolor='r', capsize=2)

        w2 = MyPlot(pierwiastki_wysokosci, srednie_t, niepewnosci_calkowite)
        w2.setTitle(r'Wykres zależności średniego czasu spadania od $\sqrt{H}$')
        w2.addStyle(r'$\sqrt{H}$ - wysokości [m]', r'$t_{śr}$ - średni czas spadania [s]')
        w2.plotBars(ecolor='r', capsize=2)

        a, b = linreg(pierwiastki_wysokosci, srednie_t)
        x = np.linspace(min(pierwiastki_wysokosci) - line_offset, max(pierwiastki_wysokosci) + line_offset)
        y = x * a + b

        w3 = MyPlot(x, y, niepewnosc_calkowita)

        w3.setTitle(r'Wykres regresji liniowej')
        # plt.margins(-1 * line_offset)
        w3.addStyle(r'$\sqrt{H}$ - pierwiastek wysokosci [m]', r'$t_{śr}$ - średni czas spadania [s]')
        w3.plotLine(extended=True).plotBars(pierwiastki_wysokosci, srednie_t, ecolor='r', capsize=2)
        l = LatexParser("../")
        print(l.gen_tex_boilerplate(X=pierwiastki_wysokosci, Y=srednie_t, uncertain=True, extended=False, signX=r"$\sqrt{H}$", signY=r"$\bar{t}$", rounding=5))

        plt.show()



    
if(__name__ == "__main__"):
    main()
