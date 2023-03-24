#! /usr/bin/env python3

import sys

from viaduc import Viaduc


class Presentation(Viaduc.Presentation):
    width = height = 300
    title = 'no bootstrap'
    html = '''
<!DOCTYPE html>
  <head>
    <title>{{title}}</title>
  </head>
  <body style="background: #de3163; color: #fbfcfc; overflow: hidden">
    <div style="font-size: 15em; margin: auto; width: 50%;">V</div>
  </body>  
</html>
'''


if __name__ == '__main__':
    Viaduc(presentation=Presentation(), args=sys.argv + ['--no-bootstrap', '--frameless'])
