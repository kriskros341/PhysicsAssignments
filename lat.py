from jinja2.loaders import FileSystemLoader
from latex.jinja2 import make_env
from typing import Optional, List
import os
import sys
import math

class LatexParser:
    def __init__(self, relpath: Optional[str] = ''):
        self.relpath = relpath

    def gen_tex_table(self, headers, data):
        realpath = os.path.dirname(os.path.realpath(sys.argv[0])) + self.relpath
        env = make_env(loader=FileSystemLoader(realpath + "\\" + self.relpath if self.relpath else "."))
        tpl = env.get_template('doc.latex')
        col_count = len(headers)
        row_count = -1
        if col_count == 1:
            row_count = len(data)

        else:
            row_count = len(data[0])

        return tpl.render(headers=headers, data=data, col_count=col_count, row_count=row_count)

    def gen_tex_boilerplate(self, X: List[float], Y: List[float], signX: str, signY: str, extended: bool = False, uncertain: bool = False, rounding: int = 3):
        realpath = os.path.dirname(os.path.realpath(sys.argv[0])) + self.relpath
        env = make_env(loader=FileSystemLoader(realpath + "\\" + self.relpath if self.relpath else "."))
        tpl = env.get_template('doc2.latex')
        N = len(X)
        SX = sum(X)
        SY = sum(Y)
        SXX = sum((x*x for x in X))
        SXY = sum(X[i]*Y[i] for i in range(len(X)))
        a = (N * SXY - SX * SY) / (N * SXX - SX * SX)
        b = (SXX * SY - SX * SXY) / (N * SXX - SX * SX)

        e = [Y[i] - a * X[i] - b for i in range(len(X))]
        See = sum(x * x for x in e)
        common = N / (N - 2) * See / (N * sum(x * x for x in X) - sum(X))
        Ua = math.sqrt(common)
        Ub = math.sqrt(sum(x * x for x in X) * common)
        rounding_name = [
            "pierwszego",
            "drugiego",
            "trzeciego",
            "czwartego",
            "piatego",
            "szóstego",
            "siódmego",
            "usmego"
        ]
        return tpl.render(
            N=N, X=[round(x, rounding) for x in X], Y=[round(x, rounding) for x in Y],
            SX=round(SX, rounding), SY=round(SY, rounding), SXX=round(SXX, rounding), SXY=round(SXY, rounding),
            signX=signX, signY=signY,
            a=round(a, rounding), b=round(b, rounding),
            extended=extended, uncertain=uncertain,
            See=round(See, rounding), Ua=round(Ua, rounding), Ub=round(Ub, rounding),
            rounding=rounding, rounding_name=rounding_name[rounding-1]
        )



