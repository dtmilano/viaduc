#! /usr/bin/env python3

import sys

from viaduc import Viaduc


class Presentation(Viaduc.Presentation):
    width = 800
    height = 600
    title = "columns"


if __name__ == "__main__":
    Viaduc(presentation=Presentation(), args=sys.argv + ["--with-streamlit=columns.py"])
