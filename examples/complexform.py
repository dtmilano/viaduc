#! /usr/bin/env python3
import sys

from viaduc import Viaduc


class Api(Viaduc.Api):
    def do_something(self, vals):
        print("do_something: {}".format(vals))
        v = self.map_vals(vals)
        if not v["inputEmail4"]:
            raise ValueError("Empty email")
        if not v["inputPassword4"]:
            raise ValueError("Empty password")
        if v["inputCheck"]:
            return Viaduc.callback("callback", {"message": "This is a sample callback"})
        else:
            return Viaduc.done("Operation completed")


class Presentation(Viaduc.Presentation):
    width = 800
    height = 520
    title = "complex form example"
    # NOTE: Usually we want html to be a string so everything is contained in one file, however in this case we are
    # reading it from a file as an example of how it can be done.
    file = "complexform-mui.html"


if __name__ == "__main__":
    Viaduc(api=Api(), presentation=Presentation(), args=sys.argv)
