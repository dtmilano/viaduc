#! /usr/local/bin/python3

from viaduc import Viaduc


class Presentation(Viaduc.Presentation):
    title = 'hello world'
    html = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    {{bootstrap_css}}

    <title>{{title}}</title>
  </head>
  <body>
    <div class="jumbotron">
        <h1>{{title}}</h1>
        <p class="lead">Welcome to <em>Viaduc</em>, the simplest way of creating a GUI in python.</p>
    </div>
    
    <!-- Option 1: jQuery and Bootstrap Bundle (includes Popper) -->
    {{bootstrap_js}}

  </body>  
 </html>
'''


if __name__ == '__main__':
    Viaduc(presentation=Presentation())
