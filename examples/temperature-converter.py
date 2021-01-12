#! /usr/bin/env python3
import sys

from viaduc import Viaduc


def fahrenheit_to_celsius(fahrenheit):
    return round((5 / 9) * (float(fahrenheit) - 32), 2)


class Api(Viaduc.Api):
    def convert(self, vals) -> dict[str, str]:
        v = self.map_vals(vals)
        if not v['_fahrenheit']:
            raise ValueError('Enter a temperature')
        response = {
            'action': 'CALLBACK',
            'function': 'showCelsius',
            'params': {
                'celsius': fahrenheit_to_celsius(v['_fahrenheit'])
            }
        }
        return response


class Presentation(Viaduc.Presentation):
    width = 320
    height = 468
    title = 'temperature converter'
    html = '''
    <!-- copy file here -->
    '''
    file = "temperature-converter.html"


if __name__ == '__main__':
    Viaduc(api=Api(), presentation=Presentation(), args=sys.argv + ['--frameless'])
