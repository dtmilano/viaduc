#! /usr/bin/env python3

import sys

from viaduc import Viaduc


class Presentation(Viaduc.Presentation):
    width = height = 800
    title = "streamlit"


if __name__ == "__main__":
    Viaduc(presentation=Presentation(), args=sys.argv + ["--with-streamlit=hello"])
