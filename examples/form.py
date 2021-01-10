#! /usr/bin/env python3
import sys

from viaduc import Viaduc


class Api(Viaduc.Api):
    def do_something(self, vals) -> dict[str, str]:
        v = self.map_vals(vals)
        if not v['_email']:
            raise ValueError('Empty email')
        if not v['_password']:
            raise ValueError('Empty password')
        response = {
            'action': 'DONE',
            'message': 'Operation completed'
        }
        return response


class Presentation(Viaduc.Presentation):
    width = 800
    height = 560
    title = 'form example'
    # NOTE: Usually we want html to be a string so everything is contained in one file, however in this case we are
    # reading it from a file as an example of how it can be done.
    file = "form.html"


if __name__ == '__main__':
    Viaduc(api=Api(), presentation=Presentation(), args=sys.argv + ['--frameless'])
