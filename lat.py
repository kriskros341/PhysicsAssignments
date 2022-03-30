from jinja2.loaders import FileSystemLoader
from latex.jinja2 import make_env
from typing import Optional, List
import os
import sys

class LatexParser:
    def __init__(self, relpath: Optional[str] = ''):
        realpath = os.path.dirname(os.path.realpath(sys.argv[0])) + relpath
        self.env = make_env(loader=FileSystemLoader(realpath + "\\" + relpath if relpath else "."))
        self.tpl = self.env.get_template('doc.latex')

    def gen_tex_table(self, headers, data):
        col_count = len(headers)
        row_count = -1
        if col_count == 1:
            row_count = len(data)

        else:
            row_count = len(data[0])

        return self.tpl.render(headers=headers, data=data, col_count=col_count, row_count=row_count)



